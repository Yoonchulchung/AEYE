import base64
import io

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from PIL import Image

from inference.infra.repository.result_repo import ResultRepository
from inference.infra.repository.request_repo import RequestRepository

router = APIRouter()

@router.get("/inference/result/{job_id}")
async def result(job_id: str):
  
    result_repo = ResultRepository()
    result = result_repo.search_by_job_id(job_id)
    
    request_repo = RequestRepository()
    request = request_repo.search_by_job_id(job_id)
    
    if not result:
        return _nothing()
    
    img_path = request.img_path
    img = Image.open(img_path).convert("RGB")
    data_url = pil_to_data_url(img, fmt="PNG")
    
    classification = result.classification
    llm_result = result.result
    summary= result.result_summary

    page = _show_image(data_url, classification, llm_result, summary)
    return HTMLResponse(page)
    
def _nothing():
    return HTMLResponse(
                content="""
                <html>
                <head><meta charset="utf-8"><title>Waiting…</title></head>
                <body style="font-family: system-ui, sans-serif; padding: 24px;">
                    <h2>대기 중…</h2>
                    <p>표시할 결과가 아직 큐에 없습니다.</p>
                </body>
                </html>
                """,
                status_code=200,
            )
    

def _show_image(data_url: str, classification : str, result: str, summary : str) -> str:
    html_page = f"""
    <html>
      <head>
        <meta charset="utf-8">
        <title>Inference Result</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
          body {{
            font-family: system-ui, sans-serif;
            padding: 24px;
            background: #f7f7f8;
          }}
          .card {{
            max-width: 960px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.08);
            padding: 20px;
          }}
          img {{
            max-width: 100%;
            height: auto;
            border-radius: 12px;
            display: block;
            margin: 0 auto;
          }}
          .message {{
            margin-top: 16px;
            font-size: 16px;
            color: #222;
            white-space: pre-wrap;
            text-align: left;
          }}
          .toolbar {{
            display: flex;
            gap: 8px;
            margin-bottom: 12px;
            justify-content: flex-end;
          }}
          button {{
            padding: 8px 12px;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
            background: #fff;
            cursor: pointer;
          }}
          button:hover {{
            background: #f3f4f6;
          }}
        </style>
      </head>
      <body>
        <div class="card">
          <div class="toolbar">
            <button onclick="location.reload()">새로고침</button>
          </div>
          <img src="{data_url}" alt="inference image" />
          <div class="message"><strong>추론 결과:</strong><br>{classification}</div>
          <div class="message"><strong>진단 방법:</strong><br>{result}</div>
          <div class="message"><strong>요약:</strong><br>{summary}</div>
        </div>
      </body>
    </html>
    """
    return html_page


def pil_to_streaming_response(img: Image.Image, fmt: str = "PNG"):
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    buf.seek(0)
    mime = "image/png" if fmt.upper() == "PNG" else f"image/{fmt.lower()}"

def pil_to_data_url(img: Image.Image, fmt: str = "PNG") -> str:
    if isinstance(img, list):
        if len(img) == 1 and isinstance(img[0], Image.Image):
            img = img[0]
        else:
            raise TypeError(f"Expected single PIL.Image.Image, got list: len={len(img)}")
    if not isinstance(img, Image.Image):
        raise TypeError(f"Expected PIL.Image.Image, got {type(img)}")

    buf = io.BytesIO()
    img.save(buf, format=fmt)
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    mime = "image/png" if fmt.upper() == "PNG" else f"image/{fmt.lower()}"
    return f"data:{mime};base64,{b64}"
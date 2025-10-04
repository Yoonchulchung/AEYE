#############################################################
# AEYE Web Nextjs Dockerfile
# Created By Yoonchul Chung
# Created At 2024.08.03
# Welcome to Visit Github : https://github.com/Yoonchulchung
#############################################################
FROM node:18-alpine

WORKDIR /app/
COPY /AEYE_Front/ ./

RUN npm install
ENV NODE_ENV=production
RUN npm run build

EXPOSE 3000
ENV PORT 3000
CMD ["npm", "start"]
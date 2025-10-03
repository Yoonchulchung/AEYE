import { useCookies } from "next-client-cookies";

const useUser = () => {
  // Using useCookies to access cookies
  const cookies = useCookies();

  // Get the user's email from the cookie
  const userEmail = cookies.get("AEYE_CU");
  const profileImageSrc = cookies.get("AEYE_PI");
  // Find the user in the users.json by email

  // If user is found, return email and profile image, otherwise return null values
  if (userEmail && profileImageSrc) {
    return {
      email: userEmail,
      profileImage: profileImageSrc,
    };
  } else {
    return null;
  }
};

export default useUser;

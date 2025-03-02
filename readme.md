# Google Drive API Endpoints Documentation

This document provides details on the available API endpoints for integrating Google Drive with your Django application. The APIs allow users to upload files to Google Drive, list their Google Drive files, and download files from Google Drive.

## Base URL

```
https://enfund-3bc4b732ed3d.herokuapp.com/google-drive/
```

Replace `enfund-3bc4b732ed3d.herokuapp.com` with your actual server URL if needed.

## Authentication

All endpoints require authentication. Users must be authenticated via the Google OAuth system and have their Google Drive linked.

---

## 1. Upload File to Google Drive

**Endpoint:**

```
POST /google-drive/upload/
```

**Description:**
Uploads a file to the authenticated user's Google Drive.

**Headers:**

```json
{
  "Authorization": "Bearer <your_access_token>",
  "Content-Type": "multipart/form-data"
}
```

**Body (Multipart Form Data):**

| Key  | Type  | Description          |
|------|-------|----------------------|
| file | File  | The file to upload   |

**Response (Success - 200 OK):**

```json
{
  "file_id": "1X2Y3Z4ABC",
  "message": "File uploaded successfully"
}
```

**Response (Error - 400 Bad Request):**

```json
{
  "error": "No file provided"
}
```

---

## 2. List Files in Google Drive

**Endpoint:**

```
GET /google-drive/files/
```

**Description:**
Fetches a list of all files stored in the authenticated user's Google Drive.

**Headers:**

```json
{
  "Authorization": "Bearer <your_access_token>"
}
```

**Response (Success - 200 OK):**

```json
{
  "files": [
    {
      "id": "1X2Y3Z4ABC",
      "name": "example.pdf"
    },
    {
      "id": "4X5Y6Z7DEF",
      "name": "photo.png"
    }
  ]
}
```

**Response (Error - 400 Bad Request):**

```json
{
  "error": "Google Drive not linked"
}
```

---

## 3. Download File from Google Drive

**Endpoint:**

```
GET /google-drive/download/<file_id>/
```

**Description:**
Downloads a file from Google Drive and returns a link to access the file from local storage.

**Headers:**

```json
{
  "Authorization": "Bearer <your_access_token>"
}
```

**Response (Success - 200 OK):**

```json
{
  "message": "File downloaded successfully",
  "file_url": "https://enfund-3bc4b732ed3d.herokuapp.com/media/downloads/example.pdf"
}
```

**Response (Error - 400 Bad Request):**

```json
{
  "error": "Google Drive not linked"
}
```

---

## Error Handling

| Status Code | Message                       | Description                                      |
|------------|-------------------------------|--------------------------------------------------|
| 400        | "No file provided"            | The request does not contain a file.            |
| 400        | "Google Drive not linked"     | The user has not linked their Google Drive.     |
| 500        | "Internal Server Error"       | An unexpected error occurred on the server.     |

---

## Postman Collection

To test these APIs in Postman:
1. Open Postman and create a new request.
2. Set the request type (POST/GET) and URL.
3. Add the Authorization token in the headers.
4. For upload, use form-data to attach a file.
5. Send the request and check the response.

---

## Notes
- Ensure the user has authenticated and linked their Google Drive account before using these APIs.
- The download endpoint fetches files from Google Drive and stores them in the server’s `media/downloads` directory.
- The API uses OAuth tokens for Google Drive authentication, stored in the `GoogleDriveToken` model.

---

This concludes the documentation for the Google Drive API endpoints. If you need further assistance, refer to the project code or contact the developer team.

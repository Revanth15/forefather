# API details

Base URL: `https://admin.111416.xyz`. No authentication in this single-owner release. API responses are JSON; downloads are HTML attachments. No CORS support. Command-line clients may omit Origin. Browser mutations must originate on the admin origin.

| Method | Path                      | Body / behavior                                                  |
| ------ | ------------------------- | ---------------------------------------------------------------- |
| POST   | /v1/documents             | JSON `{title, filename, html}`, returns 201 and metadata         |
| GET    | /v1/documents             | Optional `search`, `limit` 1–100, opaque `cursor`                |
| GET    | /v1/documents/:id         | Metadata and quoted version ETag                                 |
| GET    | /v1/documents/:id/content | Exact HTML bytes, attachment                                     |
| PUT    | /v1/documents/:id/content | Raw UTF-8 HTML, `Content-Type: text/html`, `If-Match: "VERSION"` |
| PATCH  | /v1/documents/:id         | JSON title and/or filename, `If-Match: "VERSION"`                |
| DELETE | /v1/documents/:id         | `If-Match: "VERSION"`, returns 204                               |
| GET    | /health                   | Basic service status                                             |

Metadata fields: `id`, `title`, `filename`, `sizeBytes`, `contentSha256`, `version`, `createdAt`, `updatedAt`, `viewUrl`, `downloadUrl`. Download URL is relative to the management origin. List response is `{documents, nextCursor}`. Follow `nextCursor` with the same search and limit until null.

Titles and filenames are 1–200 characters, with no control characters. Filenames must be plain `.html` filenames without slashes. IDs are lowercase UUIDv4. HTML is limited to 1,048,576 UTF-8 bytes. Whitespace and a UTF-8 BOM are preserved. Invalid UTF-8 and unpaired Unicode surrogates are rejected.

Errors use `{error:{code,message,requestId}}`. 400 means invalid input; 403 means a cross-origin browser mutation; 404 means absent document; 412 means a stale version; 413 means oversized input; 415 means wrong content type; 428 means missing If-Match. No automatic write retries or idempotency keys. Metadata changes also increment the version.

On the content origin (`https://111416.xyz`), documents can also opt into D1-backed state persistence via `/__hd/storage.js` and `/api/v1/documents/:id/state` (`POST`, `GET`, `PUT`, `DELETE` with `X-State-Token` and `If-Match`, capped at 512 KiB JSON).

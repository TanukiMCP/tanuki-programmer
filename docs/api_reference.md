# Tanuki-Programmer API Reference

This document provides a detailed reference for the Tanuki-Programmer API, built with FastAPI. It covers available endpoints, request/response models, and security considerations.

## Base URL

The base URL for the API will depend on your deployment.
-   **Local:** `http://localhost:8000` (when running `uvicorn src.api:app --host 0.0.0.0 --port 8000`)
-   **Cloud Run:** The URL provided by Google Cloud Run after deployment (e.g., `https://tanuki-programmer-service-xxxxxxxx-uc.a.run.app`)

## Authentication

All API endpoints require authentication using an API Key. The API Key must be provided in the `X-API-Key` HTTP header.

**Example Header:**
`X-API-Key: supersecretapikey123`

**Error Responses:**
-   `401 Unauthorized`: If the `X-API-Key` header is missing or the provided API Key is invalid.

## Authorization

Access to certain endpoints may require specific roles. Roles are associated with the API Key used for authentication.

**Example Roles:**
-   `user`: Can submit programming tasks.
-   `admin`: Can perform administrative actions (conceptual, not implemented in this basic API).

**Error Responses:**
-   `403 Forbidden`: If the authenticated user (via API Key) does not have the required roles for the endpoint.

## Rate Limiting

To prevent abuse and ensure fair usage, API requests are rate-limited. The current conceptual limit is 5 requests per minute per API Key.

**Error Responses:**
-   `429 Too Many Requests`: If the API Key exceeds the allowed request rate.

## Endpoints

### 1. `POST /run_task`

Submits a programming task to the Tanuki-Programmer for execution.

-   **Requires:** Authentication (`X-API-Key`), Authorization (`user` role), Rate Limiting.
-   **Description:** This endpoint allows external systems or users to programmatically request the Tanuki-Programmer to perform a coding task. The task is processed by the underlying orchestration and agent system.

#### Request Body (`TaskRequest`)

```json
{
  "task_description": "string",
  "context": "string (optional)",
  "file_paths": [
    "string"
  ]
}
```

| Field            | Type          | Description                                                              | Required |
| :--------------- | :------------ | :----------------------------------------------------------------------- | :------- |
| `task_description` | `string`      | A clear and concise description of the programming task to be performed. | Yes      |
| `context`        | `string`      | Optional. Additional context relevant to the task, such as conversation history, specific requirements, or code snippets. | No       |
| `file_paths`     | `array<string>` | Optional. A list of file paths that the Tanuki-Programmer should consider or modify for the task. | No       |

#### Response Body (`TaskResponse`)

```json
{
  "task_id": "string",
  "status": "string",
  "result": "string (optional)",
  "error": "string (optional)",
  "timestamp": float
}
```

| Field       | Type     | Description                                                              |
| :---------- | :------- | :----------------------------------------------------------------------- |
| `task_id`   | `string` | A unique identifier for the submitted task.                              |
| `status`    | `string` | The current status of the task (e.g., "completed", "failed", "processing"). |
| `result`    | `string` | Optional. The output or result of the programming task if successful.    |
| `error`     | `string` | Optional. An error message if the task failed.                           |
| `timestamp` | `float`  | Unix timestamp indicating when the response was generated.               |

#### Example Request

```bash
curl -X POST "http://localhost:8000/run_task" \
     -H "X-API-Key: supersecretapikey123" \
     -H "Content-Type: application/json" \
     -d '{
       "task_description": "Write a Python function to calculate the nth Fibonacci number.",
       "context": "Use an iterative approach for efficiency.",
       "file_paths": ["src/utils.py"]
     }'
```

#### Example Success Response

```json
{
  "task_id": "task_1678886400",
  "status": "completed",
  "result": "\nTask: \"Write a Python function to calculate the nth Fibonacci number.\"\nContext: Use an iterative approach for efficiency.\nFiles: src/utils.py\n\n---\nSimulated Tanuki-Programmer Output:\n\nAnalyzing task requirements...\nBreaking down into sub-tasks...\nGenerating code for main logic...\nRunning tests...\nRefactoring for production quality...\n\nTask completed successfully!\n(This is a simulated response. Actual output will vary based on the task and Tanuki-Programmer's capabilities.)\n    ",
  "error": null,
  "timestamp": 1678886400.0
}
```

#### Example Error Response (Invalid API Key)

```json
{
  "detail": "Invalid API Key"
}
```

### 2. `GET /health`

Checks the health status of the API.

-   **Requires:** Authentication (`X-API-Key`).
-   **Description:** A simple endpoint to verify that the API service is running and responsive.

#### Response Body

```json
{
  "status": "string",
  "message": "string"
}
```

| Field     | Type     | Description                                |
| :-------- | :------- | :----------------------------------------- |
| `status`  | `string` | The health status (e.g., "ok").            |
| `message` | `string` | A descriptive message about the health.    |

#### Example Request

```bash
curl -X GET "http://localhost:8000/health" \
     -H "X-API-Key: supersecretapikey123"
```

#### Example Success Response

```json
{
  "status": "ok",
  "message": "Tanuki-Programmer API is healthy."
}
```

This API reference provides the necessary details for developers to integrate with the Tanuki-Programmer system.

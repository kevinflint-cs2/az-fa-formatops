import json
import logging

import azure.functions as func

from functions import html_to_docx, md_to_docx, md_to_pptx, yaml_checker

app = func.FunctionApp()


@app.route(route="html_to_docx/convert", methods=["POST"])
def html_to_docx_convert(req: func.HttpRequest) -> func.HttpResponse:
    """
    Convert HTML to DOCX format and return as base64-encoded string.

    Request Body:
        {
            "html": "<html>...</html>"
        }

    Returns:
        JSON response with status and result/error:
        - 200: Success with base64-encoded DOCX
        - 400: Invalid or missing input
        - 500: Conversion error
    """
    logging.info("HTML to DOCX conversion request received")

    try:
        # Parse JSON request body
        try:
            payload = req.get_json()
        except ValueError as e:
            raise ValueError("Invalid JSON in request body") from e

        if not payload:
            raise ValueError("Empty request body")

        # Call module handler
        result = html_to_docx.handle_request(payload)

        logging.info(f"Conversion successful, output size: {result['result']['size_bytes']} bytes")

        return func.HttpResponse(json.dumps(result), mimetype="application/json", status_code=200)

    except ValueError as e:
        # Client error (invalid input)
        logging.warning(f"Bad request: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=400)

    except RuntimeError as e:
        # Conversion error (pypandoc failure)
        logging.error(f"Conversion error: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)

    except Exception as e:
        # Unexpected error
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        error = {"status": "error", "error": {"msg": "Internal server error"}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)


@app.route(route="yaml/validate", methods=["POST"])
def yaml_validate(req: func.HttpRequest) -> func.HttpResponse:
    """
    Validate YAML content and report syntax issues.

    Request Body:
        {
            "yaml": "key: value"
        }

    Returns:
        JSON response:
        - 200: Always returns a validation result with keys 'valid' and 'issues'
        - 400: Missing/invalid input
        - 500: Unexpected server error
    """
    logging.info("YAML validation request received")

    try:
        try:
            payload = req.get_json()
        except ValueError as e:
            raise ValueError("Invalid JSON in request body") from e

        if not payload:
            raise ValueError("Empty request body")

        result = yaml_checker.handle_request(payload)

        return func.HttpResponse(json.dumps(result), mimetype="application/json", status_code=200)

    except ValueError as e:
        logging.warning(f"Bad request: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=400)

    except Exception as e:  # Unexpected error
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        error = {"status": "error", "error": {"msg": "Internal server error"}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)


@app.route(route="md_to_docx/convert", methods=["POST"])
def md_to_docx_convert(req: func.HttpRequest) -> func.HttpResponse:
    """
    Convert Markdown to DOCX format and return as base64-encoded string.

    Request Body:
        {
            "markdown": "# Title\nBody text"
        }

    Returns:
        JSON response with status and result/error:
        - 200: Success with base64-encoded DOCX
        - 400: Invalid or missing input
        - 500: Conversion error
    """
    logging.info("Markdown to DOCX conversion request received")

    try:
        try:
            payload = req.get_json()
        except ValueError as e:
            raise ValueError("Invalid JSON in request body") from e

        if not payload:
            raise ValueError("Empty request body")

        result = md_to_docx.handle_request(payload)

        logging.info(
            "Markdown to DOCX conversion successful, output size: %s bytes",
            result["result"]["size_bytes"],
        )

        return func.HttpResponse(json.dumps(result), mimetype="application/json", status_code=200)

    except ValueError as e:
        logging.warning(f"Bad request: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=400)

    except RuntimeError as e:
        logging.error(f"Conversion error: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        error = {"status": "error", "error": {"msg": "Internal server error"}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)


@app.route(route="md_to_pptx/convert", methods=["POST"])
def md_to_pptx_convert(req: func.HttpRequest) -> func.HttpResponse:
    """
    Convert Markdown to PPTX format and return as base64-encoded string.

    Request Body:
        {
            "markdown": "# Title\nBody text"
        }

    Returns:
        JSON response with status and result/error:
        - 200: Success with base64-encoded PPTX
        - 400: Invalid or missing input
        - 500: Conversion error
    """
    logging.info("Markdown to PPTX conversion request received")

    try:
        try:
            payload = req.get_json()
        except ValueError as e:
            raise ValueError("Invalid JSON in request body") from e

        if not payload:
            raise ValueError("Empty request body")

        result = md_to_pptx.handle_request(payload)

        logging.info(
            "Markdown to PPTX conversion successful, output size: %s bytes",
            result["result"]["size_bytes"],
        )

        return func.HttpResponse(json.dumps(result), mimetype="application/json", status_code=200)

    except ValueError as e:
        logging.warning(f"Bad request: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=400)

    except RuntimeError as e:
        logging.error(f"Conversion error: {str(e)}")
        error = {"status": "error", "error": {"msg": str(e)}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        error = {"status": "error", "error": {"msg": "Internal server error"}}
        return func.HttpResponse(json.dumps(error), mimetype="application/json", status_code=500)

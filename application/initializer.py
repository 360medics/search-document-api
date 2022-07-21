from application.main.services.medg_document_matching import MedGDocumentService
from config import Config

medg_document_service = MedGDocumentService(Config.ENV_STATE, Config.API_DEBUG_MODE)

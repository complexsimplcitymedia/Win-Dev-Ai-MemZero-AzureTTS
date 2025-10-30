# Services Directory

All services run as independent modules within the monorepo.

## Structure

Each service directory contains:
- Source code
- \un_service.py\ - Service entry point
- Configuration files (.env.example)
- README.md - Service-specific documentation

## Running Services

### From root project:
\\\ash
python services/azure-tts/run_service.py
python services/memory/run_service.py
\\\

### From within service directory:
\\\ash
cd services/azure-tts
python run_service.py
\\\

## Services

- **azure-tts** - Text-to-speech MCP server
- **memory** - Memory/learning service
- Add more services here as needed

Each service is self-contained and can be developed independently.

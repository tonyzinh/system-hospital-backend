from django.core.management.base import BaseCommand, CommandError
from apps.ai.ingestion_web import ingest_url_to_txt
from apps.ai.rag import rebuild_index

class Command(BaseCommand):
    help = "Ingesta conteúdo da web (uma ou mais URLs) e reconstrói o índice."

    def add_arguments(self, parser):
        parser.add_argument("urls", nargs="+", help="Lista de URLs para importar")

    def handle(self, *args, **options):
        urls = options["urls"]
        total_chunks = 0
        for url in urls:
            self.stdout.write(self.style.HTTP_INFO(f"Baixando: {url}"))
            try:
                paths = ingest_url_to_txt(url)
                total_chunks += len(paths)
                self.stdout.write(self.style.SUCCESS(f"OK - {len(paths)} chunks salvos"))
            except Exception as e:
                raise CommandError(f"Falhou em {url}: {e}")
        n = rebuild_index()
        self.stdout.write(self.style.SUCCESS(f"Índice reconstruído com {n} textos (novos chunks: {total_chunks})."))

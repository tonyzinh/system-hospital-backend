#!/usr/bin/env python3
"""
Script de monitoramento da saúde do Ollama
"""

import requests
import time
import json
from datetime import datetime

API_BASE = "http://127.0.0.1:8000/api/v1/ai"


def test_health():
    """Testa o health check"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=30)
        return response.status_code == 200, response.json()
    except Exception as e:
        return False, {"error": str(e)}


def test_simple_question():
    """Testa pergunta simples"""
    try:
        start = time.time()
        response = requests.post(
            f"{API_BASE}/answer", json={"question": "Oi, como você está?"}, timeout=60
        )
        duration = time.time() - start

        if response.status_code == 200:
            return True, {
                "duration": f"{duration:.2f}s",
                "answer": response.json().get("answer", "")[:100],
            }
        else:
            return False, {"duration": f"{duration:.2f}s", "error": response.text}
    except Exception as e:
        return False, {"error": str(e)}


def test_advanced_question():
    """Testa pergunta no endpoint avançado"""
    try:
        start = time.time()
        response = requests.post(
            f"{API_BASE}/answer-advanced",
            json={"question": "Me fale brevemente sobre dipirona"},
            timeout=120,
        )
        duration = time.time() - start

        if response.status_code == 200:
            return True, {
                "duration": f"{duration:.2f}s",
                "answer": response.json().get("answer", "")[:100],
            }
        else:
            return False, {"duration": f"{duration:.2f}s", "error": response.text}
    except Exception as e:
        return False, {"error": str(e)}


def monitor():
    """Executa monitoramento contínuo"""
    print("🔍 Iniciando monitoramento do Sistema AI")
    print("=" * 50)

    iteration = 0
    success_count = 0
    total_count = 0

    while True:
        iteration += 1
        timestamp = datetime.now().strftime("%H:%M:%S")

        print(f"\n[{timestamp}] Iteração #{iteration}")
        print("-" * 30)

        # Test Health
        health_ok, health_data = test_health()
        print(f"💚 Health: {'OK' if health_ok else 'FAIL'}")
        if not health_ok:
            print(f"   Erro: {health_data.get('error', 'Unknown')}")

        # Test Simple
        simple_ok, simple_data = test_simple_question()
        print(
            f"💬 Simples: {'OK' if simple_ok else 'FAIL'} ({simple_data.get('duration', 'N/A')})"
        )
        if not simple_ok:
            print(f"   Erro: {simple_data.get('error', 'Unknown')}")

        # Test Advanced
        adv_ok, adv_data = test_advanced_question()
        print(
            f"🧠 Avançado: {'OK' if adv_ok else 'FAIL'} ({adv_data.get('duration', 'N/A')})"
        )
        if not adv_ok:
            print(f"   Erro: {adv_data.get('error', 'Unknown')}")

        # Estatísticas
        if simple_ok and adv_ok:
            success_count += 1
        total_count += 1

        success_rate = (success_count / total_count) * 100
        print(
            f"📊 Taxa de sucesso: {success_rate:.1f}% ({success_count}/{total_count})"
        )

        # Aguarda próxima iteração
        time.sleep(30)


if __name__ == "__main__":
    try:
        monitor()
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoramento interrompido pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro no monitoramento: {e}")

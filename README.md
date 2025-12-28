# Offline LLM Evaluation & Cost Monitoring System

## Overview
This project is an offline-first LLM evaluation and cost monitoring system built using
FastAPI, Ollama, and SQLite. It tracks LLM requests, evaluates response quality, and
estimates token-level costs without using any paid LLM APIs.

The system is designed to simulate production-grade LLMOps workflows locally.

## Why this project?
Modern LLM applications often fail silently:
- Response quality degrades over time
- Costs increase unexpectedly
- Teams lack visibility into prompt and model changes

This project addresses these problems through evaluation, observability, and cost awareness.

## Tech Stack
- LLM Runtime: Ollama (local models)
- Backend: FastAPI
- Database: SQLite
- Evaluation: Rule-based + LLM-as-a-Judge
- Dashboard: Streamlit

## Project Phases
1. Project setup and architecture
2. LLM request logging
3. Token counting and cost estimation
4. Rule-based evaluation
5. LLM-as-a-Judge evaluation
6. Regression testing
7. Analytics dashboard

## Status
🚧 Phase 0 — Project setup in progress

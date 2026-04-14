# MIDAS

## Overview

MIDAS is a personal capital management system designed to provide a unified, structured view of financial assets across accounts, institutions, and asset classes, while supporting informed decision-making around allocation, acquisition, and liquidation.

## Core Questions

At its core, the system answers three fundamental questions:

1. What do I own?
2. Where is it held?
3. How is it distributed across categories and themes?

## Tagging Model

Unlike traditional portfolio trackers, MIDAS is not centered around rigid classifications or predefined taxonomies. Instead, it adopts a flexible, user-driven tagging model inspired by folksonomy principles. Each security can be associated with multiple tags, allowing it to exist simultaneously across different conceptual dimensions.

### Example Tags

For example, a single equity position might be tagged as:

- energy
- dividend
- inflation-hedge
- canada

This creates a faceted system where assets can be queried, grouped, and analyzed dynamically, without being constrained to a single hierarchy. Categories such as sectors (materials, energy, technology), geographies, strategies, or personal theses are all expressed through tags rather than a fixed schema.

## Account and Institution Coverage

MIDAS is designed to operate across multiple accounts and institutions, consolidating holdings into a coherent internal representation while preserving their original context (e.g., TFSA, RRSP, margin account, specific banks, or brokers). This allows for both granular tracking and high-level portfolio views.

## Long-Term Direction

Over time, the system is intended to evolve beyond passive tracking into an active decision-support layer, helping identify:

- imbalances
- concentration risks
- opportunities for reallocation

These insights are based on the structure and tagging of the portfolio.

## System Architecture

The project is structured as a modular system:

- Backend API: responsible for data modeling and aggregation
- Frontend interface: responsible for visualization and interaction

## Guiding Principle

The guiding principle behind MIDAS is simple:

> Financial clarity emerges from structure, and structure must remain flexible enough to reflect how assets are actually understood and managed.
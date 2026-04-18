# Fund Report Generator

A lightweight Python tool for tracking daily fund performance without needing to run the investment engine.

---

## Overview

We developed an investment engine that aims to beat the broader market using quantitative momentum strategies.
The engine manages a shared fund and allocates assets based on strong price momentum signals and rebalances monthly.

As a result, continuously running the engine outside of the fund's rebalance window solely to monitor performance is both time-consuming and resource-intensive.

This tool tracks the fund's performance and updates holdings automatically as the engine rebalances our fund.

**The fund's holdings will be shared. The fund's rebalancing strategy and implementation will not.**

---

> **Note:** We are still in the process of refactoring and isolating code from our engine to ensure that this tool can run autonomously.

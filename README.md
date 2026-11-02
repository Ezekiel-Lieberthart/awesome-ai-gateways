# Awesome AI Gateways [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> AI gateways sit between applications and the models, MCP tools, and agents they call, and apply routing, access control, spend limits, guardrails, and logging to that traffic.

Open source and commercial gateways for LLM, MCP, and agent-to-agent (A2A) traffic, the specifications they implement, and guides for choosing one. Entries are sorted alphabetically within each section.

Each software entry ends with its license and, for open source projects, its main implementation language. `Proprietary` marks commercial products and AI features that require a paid edition.

## Contents

- [AI Gateways](#ai-gateways)
- [MCP Gateways](#mcp-gateways)
- [Agent Gateways](#agent-gateways)
- [API Gateways with AI Features](#api-gateways-with-ai-features)
- [Cloud and Platform AI Gateways](#cloud-and-platform-ai-gateways)
- [Model Routers and Aggregators](#model-routers-and-aggregators)
- [Inference Gateways](#inference-gateways)
- [Specifications and Standards](#specifications-and-standards)
- [Guides](#guides)
- [Articles](#articles)

## AI Gateways

Gateways built for model traffic: one API in front of many providers, with routing, failover, keys, budgets, and logging.

- [Agent Router](https://github.com/theagentrouter/agent-router) - Gateway built on Envoy Gateway that gives applications one OpenAI-compatible API for hosted models, self-hosted inference, and MCP servers, formerly Envoy AI Gateway and now an Agentic AI Foundation project (`Apache-2.0`, `Go`).
- [AISIX](https://github.com/api7/aisix) - Single static binary from the creators of Apache APISIX that puts one OpenAI-compatible API in front of LLM providers and routes, secures, caches, and observes LLM and agent traffic (`Apache-2.0`, `Rust`).
- [Bifrost](https://github.com/maximhq/bifrost) - Single-binary gateway for LLM, MCP, and agent traffic behind one OpenAI-compatible API, with failover, load balancing, semantic caching, virtual keys, budgets, air-gapped deployment, and a published overhead of about 11 microseconds per request at 5,000 RPS on one t3.xlarge (`Apache-2.0`, `Go`).
- [F5 AI Gateway](https://www.f5.com/products/ai-gateway) - Control plane that combines a model gateway, an MCP gateway, and guardrails under one policy model for model, agent, and tool traffic (`Proprietary`).
- [GoModel](https://github.com/ENTERPILOT/GoModel) - Lightweight gateway with OpenAI-compatible and Anthropic-compatible APIs across providers, response caching, spend tracking, and a dashboard for adding providers (`MIT`, `Go`).
- [Helicone](https://github.com/Helicone/helicone) - LLM observability platform with a built-in AI gateway that reaches 100+ models through the OpenAI API format with routing and automatic fallbacks, plus request logging and prompt management (`Apache-2.0`, `TypeScript`).
- [LiteLLM](https://github.com/BerriAI/litellm) - Python SDK and proxy server that call 100+ LLM providers in the OpenAI format, with the proxy adding virtual keys, spend tracking, guardrails, load balancing, and an admin dashboard (`MIT`, `Python`).
- [LLM Gateway](https://github.com/theopenco/llmgateway) - Gateway and dashboard that route requests to multiple LLM providers through one API, keep provider keys in one place, and track token usage and cost (`AGPL-3.0`, `TypeScript`).
- [MLflow AI Gateway](https://mlflow.org/docs/latest/genai/governance/ai-gateway/#:~:text=MLflow%27s%20AI%20Gateway%20provides%20a%20unified%20interface) - Component of the MLflow platform that gives an organization one secure endpoint for multiple LLM providers such as OpenAI and Anthropic (`Apache-2.0`, `Python`).
- [New API](https://github.com/QuantumNous/new-api) - Self-hosted gateway with a web console that exposes OpenAI-, Claude-, and Gemini-compatible APIs over many upstream providers and manages routing, access, usage, and cost per team (`AGPL-3.0`, `Go`).
- [Otari](https://github.com/mozilla-ai/otari) - OpenAI-compatible gateway from Mozilla.ai that routes one endpoint to 40+ providers, issues virtual keys, enforces budgets, and tracks usage (`Apache-2.0`, `Python`).
- [Plano](https://github.com/katanemo/plano) - Out-of-process proxy and data plane for agentic apps that handles LLM routing with its own routing model, agent orchestration, guardrails, and tracing (`Apache-2.0`, `Rust`).
- [Portkey AI Gateway](https://github.com/Portkey-AI/gateway) - Gateway that routes to 1,600+ models through one API with retries, fallbacks, load balancing, conditional routing, and guardrails, with an MCP gateway in Portkey's hosted platform (`MIT`, `TypeScript`).
- [Teapot Router](https://teapotrouter.com) - Hosted gateway for coding agents that speaks the Anthropic and OpenAI protocols on one key, with per-request cost, token, and latency logging, public machine-readable pricing, multi-upstream failover, and credit that never expires (`Proprietary`).
- [Traceloop Hub](https://github.com/traceloop/hub) - LLM gateway that exposes an OpenAI-compatible API over OpenAI, Anthropic, Azure OpenAI, Vertex AI, and Bedrock and records every call as OpenTelemetry traces (`Apache-2.0`, `Rust`).
- [TrueFoundry AI Gateway](https://www.truefoundry.com/ai-gateway) - Enterprise gateway for hundreds of models with unified governance and real-time observability, offered alongside TrueFoundry's MCP gateway and agent gateway (`Proprietary`).

## MCP Gateways

Gateways that put many MCP servers behind one endpoint and add authentication, tool filtering, and audit logs. agentgateway, Bifrost, Kong Gateway, LiteLLM, and Portkey AI Gateway, listed in other sections, also handle MCP traffic.

- [Archestra](https://github.com/archestra-ai/archestra) - Platform with an MCP gateway using OAuth and on-behalf-of authentication, an LLM gateway, an A2A gateway, an MCP registry, SSO, RBAC, and guardrails (`AGPL-3.0`, `TypeScript`).
- [ContextForge](https://github.com/IBM/mcp-context-forge) - IBM registry and proxy that federates MCP servers, A2A agents, and REST or gRPC APIs into one endpoint with central governance, discovery, and observability (`Apache-2.0`, `Python`).
- [Docker MCP Gateway](https://github.com/docker/mcp-gateway) - Docker CLI plugin behind the MCP Toolkit in Docker Desktop that runs and deploys MCP servers from the Docker MCP Catalog and serves them to clients through one gateway (`MIT`, `Go`).
- [Gram](https://github.com/speakeasy-api/gram) - Open source stack behind Speakeasy's AI control plane, which manages company-wide access to MCP servers, skills, and assistants with fine-grained permissions, threat detection, and observability (`AGPL-3.0`, `Go`).
- [Kuadrant MCP Gateway](https://github.com/Kuadrant/mcp-gateway) - Envoy-based gateway that aggregates and routes multiple MCP servers behind one endpoint and uses Istio and Gateway API policy attachment for authentication, authorization, and rate limiting (`Apache-2.0`, `Go`).
- [Lunar.dev](https://github.com/TheLunarCompany/lunar) - API consumption gateway for applications and agents whose MCPX component aggregates multiple MCP servers into one gateway with shared policy and observability (`MIT`, `TypeScript`).
- [MCP Gateway & Registry](https://github.com/agentic-community/mcp-gateway-registry) - Governed entry point and registry for MCP servers, agents, and skills, with OAuth authentication and central discovery (`Apache-2.0`, `Python`).
- [MCPHub](https://github.com/samanhappy/mcphub) - Self-hosted MCP gateway and control plane that connects local and remote MCP servers once and serves them through stable endpoints with authentication and scoped credentials (`Apache-2.0`, `TypeScript`).
- [MCPJungle](https://github.com/mcpjungle/MCPJungle) - Self-hosted MCP gateway that registers servers once and serves them to Claude, Cursor, Codex, or custom agents through a single endpoint with access control and observability (`MPL-2.0`, `Go`).
- [Microsoft MCP Gateway](https://github.com/microsoft/mcp-gateway) - Stateless reverse proxy and management layer for MCP servers on Kubernetes, with request routing, authorization, and server lifecycle management (`MIT`, `C#`).
- [Mintive](https://www.mintive.com/) - MCP gateway and LLM gateway, formerly MintMCP, that gives each agent its own identity and governs access to models and tools by role (`Proprietary`).
- [Obot](https://github.com/obot-platform/obot) - Self-hosted AI governance platform with MCP and LLM gateways, MCP and skills registries, and isolated hosting for MCP servers (`MIT`, `Go`).
- [Runlayer](https://www.runlayer.com) - AI control plane that routes MCP and LLM calls through one gateway and discovers agent, MCP, and skill activity across endpoints and clients (`Proprietary`).
- [ToolHive](https://github.com/stacklok/toolhive) - Platform that runs each MCP server in an isolated container, enforces identity and access policy per request, and adds observability for MCP in production (`Apache-2.0`, `Go`).
- [Unla](https://github.com/AmoyLab/Unla) - Lightweight gateway that turns existing MCP servers and HTTP APIs into MCP endpoints through configuration, without code changes (`MIT`, `Go`).

## Agent Gateways

Gateways for agent-to-agent (A2A) traffic and agent egress. Archestra, ContextForge, Gravitee, Kong Gateway, and Azure API Management, listed in other sections, also proxy A2A traffic.

- [agentgateway](https://github.com/agentgateway/agentgateway) - Linux Foundation proxy built on MCP and A2A that acts as an LLM gateway, an MCP gateway with tool federation and OAuth, and an A2A gateway for agent-to-agent communication (`Apache-2.0`, `Rust`).
- [Amazon Bedrock AgentCore Gateway](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html#gateway-core-concepts-connectivity-layer) - Managed AWS entry point for agent traffic that turns APIs and Lambda functions into MCP tools, fronts other agents including A2A traffic, and routes inference across model providers (`Proprietary`).
- [Google Cloud Agent Gateway](https://docs.cloud.google.com/gemini-enterprise-agent-platform/govern/gateways/agent-gateway-overview#core-governance-components) - Enforcement point in the Gemini Enterprise Agent Platform that applies access policies, mTLS, agent identities, and MCP security to agent-to-agent and agent-to-tool traffic (`Proprietary`).
- [Solo Enterprise for agentgateway](https://www.solo.io/products/agentgateway) - Commercial agentgateway offering from Solo.io for LLM, MCP, and inference traffic, with centralized provider key storage, enterprise IAM integration, and token-based rate limits (`Proprietary`).

## API Gateways with AI Features

General-purpose API gateways and API management platforms that added LLM, MCP, or A2A support.

- [Apache APISIX](https://apisix.apache.org/ai-gateway/#:~:text=Control%20token%20consumption) - API gateway whose AI plugins proxy requests to LLM providers, load balance across model instances, limit token consumption, and apply prompt controls (`Apache-2.0`, `Lua`).
- [APIPark](https://github.com/APIParkLab/APIPark) - AI gateway and API developer portal that connects 100+ models behind a standard request format, turns prompts into APIs, and shares them across teams (`Apache-2.0`, `Go`).
- [Gravitee](https://documentation.gravitee.io/apim/ai-agent-management#agent-gateway) - API management platform whose AI Agent Management pack, part of the Enterprise Edition, adds LLM proxies, MCP proxies, A2A proxies, and an agent catalog (`Proprietary`).
- [Higress](https://github.com/higress-group/higress) - CNCF sandbox API gateway built on Istio and Envoy, with WebAssembly plugins for proxying many model providers and hosting MCP servers (`Apache-2.0`, `Go`).
- [Kong Gateway](https://developer.konghq.com/ai-gateway/#three-traffic-types-unified-control) - API gateway whose AI Gateway plugins proxy LLM traffic and govern MCP and A2A traffic, with some plugins, such as AI Proxy Advanced, limited to Kong's AI Gateway Enterprise offering (`Apache-2.0`, `Lua`).
- [KrakenD AI Gateway](https://www.krakend.io/docs/enterprise/ai-gateway/#:~:text=AI%20Gateway%20capabilities%20extend%20your%20existing%20API%20infrastructure) - Enterprise Edition features for routing LLM traffic, with prompt guards, AI budget control, semantic caching, monitoring, and an MCP gateway (`Proprietary`).
- [MuleSoft Agent Fabric](https://www.mulesoft.com/platform/agent-governance) - Salesforce MuleSoft product that applies one set of policies to agents, MCP servers, and models without rebuilding or instrumenting them (`Proprietary`).
- [Traefik Hub AI Gateway](https://doc.traefik.io/traefik-hub/ai-gateway/overview#how-it-works) - Control layer on top of the Traefik Hub API Gateway that adds middlewares for chat completion and other LLM traffic, alongside a separate MCP gateway (`Proprietary`).
- [Tyk](https://tyk.io/docs/ai-management/overview#ai-management-capabilities) - API gateway with an MCP gateway for governing agent access to MCP servers, including servers generated from REST APIs, plus Tyk AI Studio for LLM access management (`MPL-2.0`, `Go`).
- [Zuplo AI Gateway](https://zuplo.com/docs/ai-gateway/overview#core-features) - Proxy between apps and LLM providers in the Zuplo API platform, with per-app policy chains for cost control, model access, guardrails, and observability (`Proprietary`).

## Cloud and Platform AI Gateways

AI gateways offered as part of a cloud, data, or developer platform.

- [Apigee](https://cloud.google.com/solutions/apigee-ai#ucj-1-0) - Google Cloud API management used as an AI gateway to govern and secure LLM APIs and give developers consistent access to models across clouds (`Proprietary`).
- [Azure API Management AI Gateway](https://learn.microsoft.com/en-us/azure/api-management/genai-gateway-capabilities#traffic-mediation-and-control) - Azure API Management policies for LLM APIs, MCP servers, and A2A agent APIs, including token rate limits, semantic caching, load balancing, and circuit breakers (`Proprietary`).
- [Cloudflare AI Gateway](https://developers.cloudflare.com/ai-gateway/#features) - Managed gateway on Cloudflare's network with analytics, caching, rate limiting, and model fallback for requests to many AI providers (`Proprietary`).
- [Databricks Unity Gateway](https://docs.databricks.com/aws/en/ai-gateway/#:~:text=Unity%20Gateway%20is%20the%20Databricks%20governance%20solution) - Governance layer built on Unity Catalog for traffic between models, agents, MCP servers, and tools, with routing, service policies, and usage monitoring (`Proprietary`).
- [Netlify AI Gateway](https://docs.netlify.com/build/ai-gateway/overview/#overview) - Netlify service that lets code deployed on Netlify call popular AI models without separate provider accounts, credit balances, or API keys (`Proprietary`).
- [Vercel AI Gateway](https://vercel.com/docs/ai-gateway#:~:text=Use%20AI%20Gateway%20across%20modalities%20and%20clients) - Managed gateway for calling models across providers from any infrastructure, with centralized credentials, request logs, spend budgets, routing, and provider failover (`Proprietary`).

## Model Routers and Aggregators

Hosted APIs for many models behind one key, and routers that pick a model for each request.

- [Amazon Bedrock Intelligent Prompt Routing](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-routing.html#prompt-routing-works) - Serverless Bedrock endpoint that routes each request between models in the same family based on predicted response quality (`Proprietary`).
- [Microsoft Foundry Model Router](https://learn.microsoft.com/en-us/azure/foundry/openai/concepts/model-router#how-model-router-works) - Trained language model, deployed like any other Foundry model, that routes each prompt in real time to the most suitable underlying LLM (`Proprietary`).
- [Nivana](https://nivana.one/docs/routing) - Hosted model router that profiles each request by task and difficulty, scores every model in its pool on measured quality, live price, and speed, and sends the request to the highest scorer (`Proprietary`).
- [Not Diamond](https://www.notdiamond.ai) - Model router for coding agents that predicts which model to use for each input and works with existing harnesses and gateways (`Proprietary`).
- [OpenRouter](https://openrouter.ai/docs/quickstart#using-the-openrouter-api) - Hosted API for hundreds of models behind one endpoint, with automatic fallbacks and cost-based provider selection (`Proprietary`).
- [Requesty](https://www.requesty.ai) - Hosted gateway and router for 600+ models through one OpenAI-compatible API, with routing, caching, failover, spend limits, and EU data residency (`Proprietary`).
- [Septor Labs](https://septorlabs.com/docs/introduction) - Hosted gateway that serves OpenAI-style and Anthropic-style clients from one key, routes by priority, weight, least-connections, or latency, fails over before the first token, and adds semantic caching, per-key budgets, and prepaid credits (`Proprietary`).
- [vLLM Semantic Router](https://github.com/vllm-project/semantic-router) - Policy-driven router from the vLLM project that selects or combines models for each call across local, private, and cloud backends (`Apache-2.0`, `Go`).

## Inference Gateways

Gateways and routers for self-hosted model serving on Kubernetes, which route on model server state such as queue depth and prefix cache.

- [AIBrix](https://github.com/vllm-project/aibrix) - Kubernetes control plane for vLLM, SGLang, or TensorRT-LLM whose OpenAI-compatible gateway routes each request from live engine state (`Apache-2.0`, `Go`).
- [Gateway API Inference Extension](https://github.com/kubernetes-sigs/gateway-api-inference-extension) - Kubernetes SIG project that uses Envoy external processing to turn a compatible Gateway API implementation into an inference gateway for self-hosted models (`Apache-2.0`, `Go`).
- [llm-d](https://github.com/llm-d/llm-d) - CNCF sandbox distributed inference stack for Kubernetes with prefix-cache-aware and load-aware request routing (`Apache-2.0`, `Python`).
- [Shepherd Model Gateway](https://github.com/smg-project/smg) - Engine-agnostic model-routing gateway that manages worker lifecycles and balances traffic across self-hosted engines such as vLLM, TensorRT-LLM, and SGLang and cloud providers (`Apache-2.0`, `Rust`).

## Specifications and Standards

- [Agent2Agent (A2A) Protocol Specification](https://a2a-protocol.org/latest/specification/#1-introduction) - Open protocol for communication between agents, including the [Agent Card](https://a2a-protocol.org/latest/specification/#441-agentcard) used for capability discovery and the [security schemes](https://a2a-protocol.org/latest/specification/#45-security-objects) agents declare.
- [Model Context Protocol Specification](https://modelcontextprotocol.io/specification/2026-07-28#overview) - Protocol for connecting models and agents to tools and data, including the [authorization flow](https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization#overview) for HTTP transports and [security guidance for proxy scenarios](https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices#stdio-transport-security-in-proxy-scenarios).
- [Open Responses](https://www.openresponses.org/#why-open-responses) - Open specification based on the OpenAI Responses API for multi-provider, interoperable LLM interfaces, with a shared schema and acceptance tests.
- [OpenAI OpenAPI Specification](https://github.com/openai/openai-openapi#get-the-specification) - OpenAPI description of the OpenAI API, the request format behind most gateways' OpenAI-compatible endpoints.
- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai#read-the-docs) - Span, metric, and event conventions for GenAI clients and MCP that gateways can emit for every model and tool call.
- [OWASP Top 10 for Agentic Applications](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/#:~:text=identifies%20the%20most%20critical%20security%20risks) - Peer-reviewed 2026 list of the most critical security risks for autonomous and agentic AI systems.
- [OWASP Top 10 for LLM Applications](https://genai.owasp.org/llm-top-10/#:~:text=LLM01%3A2025%20Prompt%20Injection) - 2025 list of the main risks in LLM applications, such as prompt injection and sensitive information disclosure, that gateway guardrails often target.

## Guides

Vendor-neutral guides from the [AI Gateways](https://github.com/ai-gateways#start-here) organization.

- [Agent Gateway](https://github.com/ai-gateways/agent-gateway#what-is-an-agent-gateway) - How agent gateways govern A2A traffic, from [how the A2A protocol works](https://github.com/ai-gateways/agent-gateway#how-the-a2a-protocol-works) to [security and access control for agents](https://github.com/ai-gateways/agent-gateway#security-and-access-control-for-agents).
- [AI Gateway](https://github.com/ai-gateways/ai-gateway#what-is-an-ai-gateway) - What an AI gateway is, the [three kinds of AI traffic](https://github.com/ai-gateways/ai-gateway#the-three-kinds-of-ai-traffic) it governs, and [how it differs from an API gateway](https://github.com/ai-gateways/ai-gateway#ai-gateway-vs-api-gateway).
- [AI Governance](https://github.com/ai-gateways/ai-governance#what-is-ai-governance) - Governance enforced at the gateway layer, including [identity and access](https://github.com/ai-gateways/ai-governance#identity-and-access), [cost governance](https://github.com/ai-gateways/ai-governance#cost-governance), and [shadow AI](https://github.com/ai-gateways/ai-governance#shadow-ai).
- [AI Guardrails](https://github.com/ai-gateways/ai-guardrails#what-are-ai-guardrails) - Input and output checks for prompt injection, PII, secrets, and unsafe content, with the [types of guardrails](https://github.com/ai-gateways/ai-guardrails#types-of-ai-guardrails) and [where to enforce them](https://github.com/ai-gateways/ai-guardrails#where-to-enforce-guardrails).
- [LLM Gateway](https://github.com/ai-gateways/llm-gateway#what-is-an-llm-gateway) - Routing, failover, budgets, and guardrails for model traffic, with a checklist for [how to evaluate an LLM gateway](https://github.com/ai-gateways/llm-gateway#how-to-evaluate-an-llm-gateway).
- [LLM Observability](https://github.com/ai-gateways/llm-observability#what-is-llm-observability) - What to capture for model calls, [OpenTelemetry for LLM applications](https://github.com/ai-gateways/llm-observability#opentelemetry-for-llm-applications), and [gateway-layer vs SDK instrumentation](https://github.com/ai-gateways/llm-observability#gateway-layer-vs-sdk-instrumentation).
- [MCP Gateway](https://github.com/ai-gateways/mcp-gateway#what-is-an-mcp-gateway) - How MCP gateways secure tool calls, covering [MCP gateway security](https://github.com/ai-gateways/mcp-gateway#mcp-gateway-security) and [reducing token cost from large tool sets](https://github.com/ai-gateways/mcp-gateway#reducing-token-cost-from-large-tool-sets).

## Articles

- [Access Foundry Models and Other Language Models Through a Gateway](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/generative-ai-gateway#key-challenges) - Azure Architecture Center guide to the reliability, security, cost, and operations problems a gateway in front of model deployments addresses, and the options for building one.
- [Guidance for Multi-Provider Generative AI Gateway on AWS](https://docs.aws.amazon.com/solutions/multi-provider-generative-ai-gateway-on-aws/#how-it-works) - AWS reference architecture that runs a LiteLLM-based gateway on Amazon ECS or Amazon EKS behind AWS WAF and an Application Load Balancer.
- [Introducing Gateway API Inference Extension](https://kubernetes.io/blog/2025/06/05/introducing-gateway-api-inference-extension/#:~:text=you%20effectively%20transform%20it%20into%20an%20Inference%20Gateway) - Kubernetes blog post on adding an inference extension to an existing gateway so it routes requests to self-hosted LLMs.
- [Use a Gateway in Front of Multiple Model Deployments or Instances](https://learn.microsoft.com/en-us/azure/architecture/ai-ml/guide/generative-ai-gateway-multiple-models#general-recommendations) - Azure Architecture Center topologies for single-region, multi-subscription, and multi-region model deployments, including when to avoid a gateway.

## Related Lists

- [Awesome A2A](https://github.com/ai-boost/awesome-a2a) - Agent2Agent protocol agents, tools, servers, and clients.
- [Awesome AI Agents](https://github.com/e2b-dev/awesome-ai-agents) - Autonomous AI agents and agent frameworks.
- [Awesome LLMOps](https://github.com/tensorchord/Awesome-LLMOps) - Tools for running LLMs in production.
- [Awesome MCP Gateways](https://github.com/e2b-dev/awesome-mcp-gateways) - Open source and commercial MCP gateways.
- [Awesome MCP Servers](https://github.com/punkpeye/awesome-mcp-servers) - Model Context Protocol servers.

## Contributing

Contributions are welcome, including from vendors who disclose their affiliation. Read the [contribution guidelines](contributing.md) before opening a pull request; an automated review checks each entry within a few minutes.

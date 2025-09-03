# Module 1: Visual Diagrams and Architecture

This file contains all the visual diagrams used in Module 1 for easy reference and reuse.

## AI Agent Architecture Diagram

```mermaid
graph TB
    subgraph "AI Agent Core"
        LLM[Large Language Model<br/>- Reasoning Engine<br/>- Decision Making<br/>- Natural Language Processing]
        PROMPT[System Prompt<br/>- Behavior Guidelines<br/>- Role Definition<br/>- Task Instructions]
        CONTEXT[Context Manager<br/>- Conversation History<br/>- State Persistence<br/>- Memory Management]
    end
    
    subgraph "Tool Layer"
        SEARCH[Search Tools<br/>- Web Search<br/>- Document Search<br/>- Knowledge Base Query]
        FILE[File Operations<br/>- Read/Write Files<br/>- Directory Management<br/>- Data Processing]
        API[API Integrations<br/>- REST APIs<br/>- GraphQL<br/>- Webhooks]
        CUSTOM[Custom Tools<br/>- Domain-Specific Logic<br/>- Business Rules<br/>- Specialized Functions]
    end
    
    subgraph "Environment"
        USER[User Input<br/>- Natural Language<br/>- Commands<br/>- Requests]
        EXTERNAL[External Systems<br/>- Databases<br/>- Web Services<br/>- File Systems]
        DATA[Data Sources<br/>- Documents<br/>- APIs<br/>- Real-time Feeds]
    end
    
    USER --> LLM
    LLM --> PROMPT
    LLM --> CONTEXT
    LLM --> SEARCH
    LLM --> FILE
    LLM --> API
    LLM --> CUSTOM
    SEARCH --> EXTERNAL
    FILE --> DATA
    API --> EXTERNAL
    CUSTOM --> EXTERNAL
    
    EXTERNAL --> LLM
    DATA --> LLM
    
    classDef core fill:#e1f5fe
    classDef tools fill:#f3e5f5
    classDef env fill:#e8f5e8
    
    class LLM,PROMPT,CONTEXT core
    class SEARCH,FILE,API,CUSTOM tools
    class USER,EXTERNAL,DATA env
```

## Docker AI Platform Architecture

```mermaid
graph TB
    subgraph "Development Environment"
        IDE[VS Code/IDE<br/>- Code Editor<br/>- Debugging Tools<br/>- Extensions]
        WATCH[Docker Compose Watch<br/>- Hot Reload<br/>- File Monitoring<br/>- Auto Rebuild]
        COMPOSE[Docker Compose<br/>- Service Orchestration<br/>- Environment Management<br/>- Network Configuration]
    end
    
    subgraph "AI Platform Core"
        DMR[Docker Model Runner<br/>- Model Hosting<br/>- API Gateway<br/>- Resource Management]
        MCP[MCP Gateway<br/>- Tool Security<br/>- Permission Management<br/>- Protocol Translation]
        AGENT[Agent Container<br/>- Strands SDK<br/>- Business Logic<br/>- Tool Orchestration]
    end
    
    subgraph "Model Layer"
        LOCAL[Local Models<br/>- Llama 2/3<br/>- Mistral<br/>- CodeLlama]
        CLOUD[Cloud APIs<br/>- OpenAI GPT<br/>- Anthropic Claude<br/>- Google Gemini]
        CUSTOM[Custom Models<br/>- Fine-tuned Models<br/>- Domain-Specific<br/>- Specialized Tasks]
    end
    
    subgraph "Tool Integration"
        MCPS[MCP Servers<br/>- Search Server<br/>- File Server<br/>- Database Server]
        APIS[External APIs<br/>- REST Services<br/>- GraphQL<br/>- Third-party Tools]
        SERVICES[External Services<br/>- Databases<br/>- Message Queues<br/>- Monitoring]
    end
    
    IDE --> WATCH
    WATCH --> COMPOSE
    COMPOSE --> AGENT
    AGENT --> DMR
    AGENT --> MCP
    DMR --> LOCAL
    DMR --> CLOUD
    DMR --> CUSTOM
    MCP --> MCPS
    MCPS --> APIS
    MCPS --> SERVICES
    
    classDef dev fill:#fff3e0
    classDef platform fill:#e3f2fd
    classDef models fill:#f1f8e9
    classDef tools fill:#fce4ec
    
    class IDE,WATCH,COMPOSE dev
    class DMR,MCP,AGENT platform
    class LOCAL,CLOUD,CUSTOM models
    class MCPS,APIS,SERVICES tools
```

## Strands SDK Component Architecture

```mermaid
graph LR
    subgraph "Strands Agent Core"
        MODEL[Model Interface<br/>- Abstraction Layer<br/>- Provider Agnostic<br/>- Configuration Management]
        TOOLS[Tool Registry<br/>- Tool Discovery<br/>- Capability Management<br/>- Execution Coordination]
        PROMPT[Prompt Manager<br/>- Template System<br/>- Context Injection<br/>- Response Formatting]
        CONTEXT[Context Store<br/>- Conversation History<br/>- State Persistence<br/>- Memory Management]
    end
    
    subgraph "External Integrations"
        DMR[Docker Model Runner<br/>- Local Model Access<br/>- Resource Optimization<br/>- Model Switching]
        MCP[MCP Gateway<br/>- Secure Tool Access<br/>- Permission Control<br/>- Protocol Handling]
        APIS[Direct APIs<br/>- Cloud Models<br/>- External Services<br/>- Custom Integrations]
    end
    
    MODEL --> DMR
    MODEL --> APIS
    TOOLS --> MCP
    TOOLS --> APIS
    PROMPT --> MODEL
    CONTEXT --> MODEL
    
    classDef core fill:#e8eaf6
    classDef external fill:#f3e5f5
    
    class MODEL,TOOLS,PROMPT,CONTEXT core
    class DMR,MCP,APIS external
```

## Workshop Learning Flow

```mermaid
graph TD
    START[Workshop Start] --> M1[Module 1: Foundations<br/>- AI Agent Concepts<br/>- Docker AI Platform<br/>- Environment Setup]
    
    M1 --> M2[Module 2: Basic Agent<br/>- First Strands Agent<br/>- Local Models<br/>- Docker Compose Watch]
    
    M2 --> M3[Module 3: External Tools<br/>- MCP Gateway<br/>- Tool Integration<br/>- Security Best Practices]
    
    
    subgraph "Hands-on Exercises"
        EX1[Environment Setup<br/>Validation]
        EX2[Build First Agent<br/>Test & Debug]
        EX3[Add MCP Tools<br/>Security Config]
    end
    
    M1 --> EX1
    M2 --> EX2
    M3 --> EX3
    
    classDef module fill:#e1f5fe
    classDef exercise fill:#f3e5f5
    classDef milestone fill:#e8f5e8
    
    class M1,M2,M3 module
    class EX1,EX2,EX3 exercise
    class START,END milestone
```

## Docker AI Platform Component Interaction

```mermaid
sequenceDiagram
    participant Dev as Developer
    participant Watch as Compose Watch
    participant Agent as Agent Container
    participant DMR as Model Runner
    participant MCP as MCP Gateway
    participant Tool as External Tool
    
    Dev->>Watch: Code Change
    Watch->>Agent: Rebuild & Restart
    Agent->>DMR: Initialize Model
    DMR-->>Agent: Model Ready
    
    Dev->>Agent: Send Request
    Agent->>DMR: Generate Response
    DMR-->>Agent: Model Output
    
    Agent->>MCP: Execute Tool
    MCP->>Tool: Secure Tool Call
    Tool-->>MCP: Tool Result
    MCP-->>Agent: Processed Result
    
    Agent-->>Dev: Final Response
    
    Note over Dev,Tool: Hot reload preserves context<br/>and maintains development flow
```

## Security Architecture with MCP Gateway

```mermaid
graph TB
    subgraph "Agent Container"
        AGENT[Strands Agent<br/>- Business Logic<br/>- Tool Requests<br/>- Response Processing]
    end
    
    subgraph "MCP Gateway Security Layer"
        AUTH[Authentication<br/>- API Key Validation<br/>- Permission Checks<br/>- Rate Limiting]
        SANDBOX[Sandboxing<br/>- Isolated Execution<br/>- Resource Limits<br/>- Network Isolation]
        AUDIT[Audit Logging<br/>- Request Tracking<br/>- Security Events<br/>- Compliance Reports]
    end
    
    subgraph "External Tools"
        SEARCH[Search APIs<br/>- Web Search<br/>- Document Search<br/>- Knowledge Bases]
        FILES[File Systems<br/>- Local Files<br/>- Cloud Storage<br/>- Databases]
        APIS[External APIs<br/>- REST Services<br/>- GraphQL<br/>- Webhooks]
    end
    
    AGENT --> AUTH
    AUTH --> SANDBOX
    SANDBOX --> AUDIT
    AUDIT --> SEARCH
    AUDIT --> FILES
    AUDIT --> APIS
    
    classDef agent fill:#e3f2fd
    classDef security fill:#ffebee
    classDef external fill:#f1f8e9
    
    class AGENT agent
    class AUTH,SANDBOX,AUDIT security
    class SEARCH,FILES,APIS external
```

# Tanuki-History: Domain-Specialized MoA for Historical Research & Social Sciences

## 1. Domain Vision & Scope

### 1.1. Core Mission
Tanuki-History is a specialized Mixture-of-Agents system designed to excel at historical research, social science analysis, and temporal reasoning. It combines comprehensive historical knowledge with rigorous research methodologies to provide accurate, contextual, and well-sourced historical analysis and insights.

### 1.2. Sub-Domain Coverage
The system encompasses the full spectrum of historical and social science disciplines with specialized agents:

| Sub-Domain | Expert Agent | Primary Capabilities |
|:---|:---|:---|
| **Planning & Strategy** | `tanuki-planner-critic` | **(Foresight Agent)** Generates and critiques multiple research paths and historiographical approaches. |
| **Ancient History** | `tanuki-ancient-historian` | Classical civilizations, archaeology, ancient sources. |
| **Medieval Studies** | `tanuki-medievalist` | Middle Ages, feudalism, religious history. |
| **Modern History** | `tanuki-modern-historian` | Renaissance to present, nation-states, revolutions. |
| **Social History** | `tanuki-social-historian` | Demographics, social movements, cultural change |
| **Political History** | `tanuki-political-historian` | Governance, diplomacy, political theory |
| **Economic History** | `tanuki-economic-historian` | Trade, finance, economic systems, labor |
| **Military History** | `tanuki-military-historian` | Warfare, strategy, military technology |
| **Historiography** | `tanuki-historiographer` | Historical methods, source criticism, interpretation. |
| **Adversarial Review** | `tanuki-history-reviewer` | **(Reviewer Loop)** Finds factual inaccuracies, weak sourcing, and logical fallacies in historical arguments. |

---

## 2. Ultra-Low-Cost Hybrid Training Strategy

This project adheres to a strict budget by pioneering a hyper-efficient hybrid training model that costs a total of **~$120 for all 32 expert agents** across four flagship domains.

### 2.1. The "One-Weekend-Rent" Model
All expensive training steps are consolidated into a single 72-hour rental of an RTX 4090 GPU (~$30 total cost).

1.  **Phase 1: Foundation Training (Synthetic Data - Cost: $0)**
    -   **Process**: A curated collection of free, open-source datasets from Hugging Face is transformed programmatically into ReAct-style training examples. This builds a foundational understanding of historical analysis and source criticism for free, completely eliminating data acquisition costs.
    
2.  **Phase 2: Teacher-Guided Refinement (Process-Oriented Reward)**
    -   **Process**: During the GPU rental, a powerful teacher model ([Qwen1.5-32B-Chat](https://huggingface.co/Qwen/Qwen1.5-32B-Chat)) is used for a short, intense burst of inference.
    -   **Student Model Choice**: We will use **Gemma-2B-It**, whose factual accuracy is ideal for this domain and can be fine-tuned for longer context.
    -   **Training Methodology (Process-Oriented Reward)**: We reward the entire research process. The training data will explicitly prefer arguments built on strong, cross-verified primary sources over those that rely on weak evidence, even if the final conclusion is plausible. This teaches the model the principles of good historiography.

---

## 3. Architecture Design

### 3.1. Zero-Cost Data Sources & Synthesis Pipeline

All foundation training data is sourced from free, open-source Hugging Face datasets. Each dataset is chosen to train specific expert agents within the MoA.

| Expert Agent | Primary HF Dataset(s) | Usage & Synthesis Strategy |
|:---|:---|:---|
| **`tanuki-ancient-historian`** | `community-datasets/ancient-texts` & `pszemraj/ldj-scaling-law-2-left-to-right` | A collection of classical texts and general knowledge. Used to train the agent on recognizing figures, events, and locations from antiquity and verifying them. |
| **`tanuki-medievalist`** | `Jean-Baptiste/camembert-base-medieval` (model, but data is extractable) | The dataset for this model is focused on medieval French. It will be used to train the agent on the specific language, culture, and concepts of the Middle Ages. |
| **`tanuki-modern-historian`** | `sayakabiz/historical_archives_of_the_european_union` | A rich source of primary documents from the modern era. Used to synthesize source analysis and contextualization tasks. |
| **`tanuki-social-historian`** | `numerai/user-contributions` & `quoref` | While not explicitly historical, these datasets about user behaviors and Q&A can be used to synthesize social history questions about trends, beliefs, and daily life. |
| **`tanuki-political-historian`** | `rahular/american-presidential-speech-corpus` | A corpus of speeches. Used to train the agent on political rhetoric, policy, and the evolution of political thought over time. |
| **`tanuki-economic-historian`** | `Financial-Pythia/financial-aphorisms` & `pile-of-law/pile-of-law` | Used to extract financial concepts and legal frameworks to train the agent on the history of trade, finance, and economic regulation. |
| **`tanuki-military-historian`** | `social_bias_frames` (filtered for conflict) | A dataset of social biases. We will filter for frames related to conflict to train the agent on analyzing the causes, events, and consequences of military engagements. |
| **`tanuki-historiographer`**| `wikipedia` (specifically pages on historical methods) & `CShorten/ML-ArXiv-Papers` | Used to train the agent on the theory of history itself—how it is written, the different schools of thought, and how to critique historical sources. |

**Synthesis Example (`tanuki-modern-historian`):**
```python
def synthesize_history_data(document_from_heu_archives):
    # This function remains the same, but now operates on a richer, free data source
    return {
        "instruction": "Analyze the attached primary source document from the post-war period.",
        "thought": "I need to perform source criticism, place the document in its proper chronological context, and cross-reference its claims with my internal knowledge base.",
        "tool_calls": [
            {"tool": "source_criticism", "document": document_from_heu_archives},
            {"tool": "chronological_context", "period": "20th Century"},
            {"tool": "citation_check", "style": "chicago"}
        ],
        "final_answer": "This document, created on..."
    }
```

### 3.2. System Overview
The architecture is a multi-stage agentic system designed for foresight, execution, and review.

```mermaid
graph TD
    A[Historical Query] --> B[Layer 1: Ingress & Sanitizer];
    B --> C[Layer 2: Foresight Agent (Planner-Critic)];
    C -- "Selects Optimal Plan" --> D[Layer 3: Orchestrator (Context Engineer)];
    
    subgraph "Layer 4: Execution & Adversarial Review"
        D -- "Routes to Expert" --> E(tanuki-modern-historian);
        E -- "Draft Analysis" --> F(tanuki-history-reviewer);
        F -- "Critique & Correction Request" --> E;
        F -- "Approved Analysis" --> G[Layer 5: Response Aggregator];
    end
    
    G --> H[Verified Historical Analysis];
```

### 3.3. Core Architectural Layers

| Layer | Component | Function |
|:---|:---|:---|
| 1 | **Ingress & Sanitizer** | Cleans user input and identifies chronological markers. |
| 2 | **Foresight Agent** | Generates 2-3 high-level research plans (e.g., "Plan A: Analyze diplomatic cables. Plan B: Focus on economic data.") and critiques them to select the most promising path. |
| 3 | **Orchestrator Agent** | Assembles the "briefing packet" (primary sources, secondary analyses, etc.) based on the selected plan and routes it to the appropriate expert. |
| 4 | **Execution & Review Loop** | An expert agent (`tanuki-modern-historian`) generates an analysis. This draft is immediately sent to an adversarial `tanuki-history-reviewer`, whose sole job is to check for factual errors and weak sourcing. If any are found, the analysis is sent back for refinement. |
| 5 | **Response Aggregator** | Formats the final, peer-reviewed, and source-verified analysis for the user. |

### 3.4. Leveraging Large Context for Advanced Historical Workflows

The ability to use a large context window is the cornerstone of the Tanuki-History's effectiveness. The Orchestrator Agent uses this vast space to construct a "briefing packet" for the expert agent, allowing it to perform nuanced source criticism and contextualization.

**Example Briefing Packet for a Source Analysis Task:**
```
<CONTEXT>
  <CONVERSATION_HISTORY>
    <!-- Full, unabridged user-AI dialogue about the research question -->
  </CONVERSATION_HISTORY>

  <PRIMARY_SOURCE_DOCUMENT>
    <!-- Full text of a letter from a historical figure -->
  </PRIMARY_SOURCE_DOCUMENT>
  
  <SECONDARY_SOURCE_ANALYSIS>
    <!-- A scholarly article discussing the historical period and the figure's biases -->
  </SECONDARY_SOURCE_ANALYSIS>
  
  <USER_QUERY>
    Analyze the attached primary source letter. What are its main claims, and how might the author's known biases, as described in the secondary source, be influencing the account?
  </USER_QUERY>
</CONTEXT>
```
This approach allows the expert agent to perform sophisticated historiographical work by directly comparing a primary source with a secondary analysis in a single pass.

### 3.5. Specialized Tools Per Sub-Domain

| Sub-Domain | Tools & Resources |
|:---|:---|
| **Ancient History** | Archaeological databases, classical texts, numismatic catalogs |
| **Medieval Studies** | Manuscript databases, paleography tools, religious texts |
| **Modern History** | Diplomatic archives, newspaper databases, government documents |
| **Social History** | Census data, demographic tools, social movement archives |
| **Political History** | Political document archives, treaty databases, electoral data |
| **Economic History** | Financial records, trade statistics, economic indicators |
| **Military History** | Battle databases, military technology records, strategic analyses |
| **Historiography** | Methodological frameworks, source criticism tools, bias analysis |

---

## 4. Historical Knowledge Architecture

### 4.1. Temporal Reasoning Engine
```python
class HistoricalReasoningEngine:
    def __init__(self):
        self.chronology_database = load_world_chronology()
        self.causality_networks = load_historical_causality_graphs()
        self.source_reliability = load_source_credibility_database()
        self.historiographical_schools = load_interpretive_frameworks()
    
    def analyze_historical_event(self, event, context):
        """Provide comprehensive historical analysis with temporal reasoning"""
        chronological_context = self.establish_chronology(event)
        causal_relationships = self.identify_causality(event, context)
        source_analysis = self.evaluate_sources(event)
        interpretive_frameworks = self.apply_historiography(event)
        return self.synthesize_analysis(chronological_context, causal_relationships,
                                      source_analysis, interpretive_frameworks)
```

### 4.2. Source Verification and Citation
- **Primary Source Authentication**: Verification of document authenticity
- **Secondary Source Evaluation**: Assessment of scholarly credibility
- **Cross-Reference Validation**: Confirmation across multiple sources
- **Bias Detection**: Identification of potential source biases
- **Citation Standards**: Chicago, MLA, and academic historical citation formats

---

## 5. Resource Requirements & Performance

### 5.1. Memory Footprint & Quantization
The system is designed to run efficiently on consumer hardware by leveraging aggressive quantization.

- **Backbone Model**: Phi-3-mini-4K, quantized to **`Q4_K_M` using the GGUF format**. This is the key to fitting within the VRAM budget.
- **VRAM Usage**: ~2.4GB
- **8 LoRA Adapters**: ~720MB system RAM
- **Historical Databases**: ~5GB system RAM (chronologies, sources, documents)
- **Verification Systems**: ~1.5GB system RAM
- **Total**: **2.4GB VRAM** + **~7.2GB system RAM**

### 5.2. Performance Targets
| Metric | Target | Benchmark |
|:---|:---|:---|
| **Factual Accuracy** | 96% on historical facts | Cross-reference verification |
| **Source Citation** | 98% proper attribution | Academic standard compliance |
| **Chronological Accuracy** | 95% temporal relationships | Timeline verification |
| **Interpretive Quality** | 88% scholarly standards | Historian evaluation |

---

## 6. Implementation Roadmap

### 6.1. Phase 1: Historical Infrastructure (Weeks 1-8)
- [ ] Build comprehensive historical databases and archives
- [ ] Implement chronological reasoning and timeline systems
- [ ] Create source verification and citation systems
- [ ] Set up cross-cultural and comparative analysis frameworks

### 6.2. Phase 2: Expert Training (Weeks 9-16)
- [ ] Generate synthetic training data for all historical periods
- [ ] Train foundation LoRA adapters with temporal reasoning
- [ ] Apply teacher-guided refinement for interpretive sophistication
- [ ] Benchmark against historical accuracy and scholarly standards

### 6.3. Phase 3: Advanced Features (Weeks 17-24)
- [ ] Implement advanced historiographical analysis
- [ ] Add interactive timeline and mapping visualization
- [ ] Create collaborative research and peer review features
- [ ] Build academic integration with historical databases

---

## 7. Cost Analysis

### 7.1. Training Costs (for this Domain)
| Component | Cost | Notes |
|:---|:---|:---|
| **GPU Rental (Pro-rated)** | ~$7.50 | 1/4 of the shared $30 weekend rental. This budget covers all expert agents for the domain, including the planner and reviewer. |
| **Data Acquisition** | **$0** | Replaced by a curated list of free, high-quality Hugging Face datasets. |
| **Storage & Contingency** | ~$5 | Pro-rated from a shared $20 budget. |
| **Total** | **~$12.50** | Fully aligned with the ultra-low-cost budget of other domains. |

### 7.2. Competitive Advantages
- **vs. Wikipedia**: Rigorous source verification and academic standards
- **vs. General Search**: Specialized historical methodology and context
- **vs. Academic Databases**: Integrated analysis and synthesis capabilities
- **vs. History Textbooks**: Dynamic, up-to-date, and comprehensive coverage

---

## 8. Ethical Considerations & Historical Responsibility

### 8.1. Historical Accuracy and Integrity
- **Source Verification**: Rigorous authentication of historical sources
- **Fact-Checking**: Multiple source confirmation for historical claims
- **Uncertainty Communication**: Clear indication of historical debates and uncertainties
- **Bias Acknowledgment**: Recognition of historical and historiographical biases

### 8.2. Cultural Sensitivity and Representation
- **Diverse Perspectives**: Inclusion of multiple cultural and national viewpoints
- **Marginalized Voices**: Attention to underrepresented historical narratives
- **Colonial Perspectives**: Critical examination of colonial and imperial histories
- **Indigenous Histories**: Respectful treatment of indigenous historical narratives

### 8.3. Contemporary Relevance and Responsibility
- **Historical Parallels**: Careful handling of historical analogies to current events
- **Political Neutrality**: Objective historical analysis without contemporary political bias
- **Educational Purpose**: Focus on learning and understanding rather than advocacy
- **Misinformation Prevention**: Active correction of historical myths and misconceptions

### 8.4. Academic and Research Ethics
- **Plagiarism Prevention**: Clear attribution of historical research and analysis
- **Original Research**: Encouragement of independent historical investigation
- **Peer Review**: Integration with academic historical review processes
- **Scholarly Standards**: Adherence to professional historical research standards

---

*Domain: Historical Research & Social Sciences | Target Users: Historians, Researchers, Students, Educators*
*Last Updated: January 2025 | Version: 1.0 | Status: Design Phase* 
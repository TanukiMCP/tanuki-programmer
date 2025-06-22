# Tanuki-Literature: Domain-Specialized MoA for Language, Literature & Humanities

## 1. Domain Vision & Scope

### 1.1. Core Mission
Tanuki-Literature is a specialized Mixture-of-Agents system designed to excel at creative writing, literary analysis, linguistic research, and humanities scholarship. It combines deep cultural knowledge with sophisticated language understanding to assist with creative and analytical tasks across literary and humanistic disciplines.

### 1.2. Sub-Domain Coverage
The system encompasses the full spectrum of literary and humanistic endeavors with specialized agents:

| Sub-Domain | Expert Agent | Primary Capabilities |
|:---|:---|:---|
| **Planning & Strategy** | `tanuki-planner-critic` | **(Foresight Agent)** Generates and critiques multiple analytical or creative paths before execution. |
| **Creative Writing** | `tanuki-creative-writer` | Fiction, poetry, screenwriting, narrative techniques. |
| **Literary Analysis** | `tanuki-literary-critic` | Close reading, thematic analysis, literary theory. |
| **Language Studies** | `tanuki-linguist` | Etymology, syntax, phonetics, translation. |
| **Historical Research** | `tanuki-historian` | Archival research, historical context, chronology. |
| **Adversarial Review** | `tanuki-humanities-reviewer`| **(Reviewer Loop)** Finds weak arguments, unsupported claims, and factual errors in generated analyses. |

---

## 2. Ultra-Low-Cost Hybrid Training Strategy

This project adheres to a strict budget by pioneering a hyper-efficient hybrid training model that costs a total of **~$120 for all 32 expert agents** across four flagship domains.

### 2.1. The "One-Weekend-Rent" Model
All expensive training steps are consolidated into a single 72-hour rental of an RTX 4090 GPU (~$30 total cost).

1.  **Phase 1: Foundation Training (Synthetic Data - Cost: $0)**
    -   **Process**: Open-source and public domain datasets (e.g., `Project Gutenberg`, `Wikisource`) are transformed programmatically into ReAct-style training examples. This builds a foundational understanding of literary analysis and tool use for free.
    
2.  **Phase 2: Teacher-Guided Refinement (Process-Oriented Reward)**
    -   **Process**: During the GPU rental, a powerful teacher model ([Yi-34B-Chat](https://huggingface.co/01-ai/Yi-34B-Chat)) is used for a short, intense burst of inference.
    -   **Student Model Choice**: We will use **Mistral-3B**, whose 128k context window is ideal for analyzing long literary texts.
    -   **Training Methodology (Process-Oriented Reward)**: We reward the entire analytical chain, not just the final conclusion. The training data will explicitly prefer well-structured arguments with strong textual evidence over superficially plausible but unsupported claims. This teaches the model to build a strong, defensible case.

---

## 3. Architecture Design

### 3.1. Zero-Cost Data Sources & Synthesis Pipeline

All foundation training data is sourced from free, open-source Hugging Face datasets. Each dataset is chosen to train specific expert agents within the MoA.

| Expert Agent | Primary HF Dataset(s) | Usage & Synthesis Strategy |
|:---|:---|:---|
| **`tanuki-creative-writer`** | `hyper-pai/wiki_art_prompt` & `ashley-canaria/18-million-prompts` | Large datasets of creative prompts. Used to train the agent to respond to a wide variety of creative writing tasks (fiction, poetry, etc.). |
| **`tanuki-literary-critic`** | `google-research-datasets/wiki_snippets` & `d0r1h/DORIS-MAE` | General knowledge and literature passages. Used to synthesize examples where the agent must perform close reading, thematic analysis, and apply literary theory. |
| **`tanuki-linguist`** | `universal_dependencies` (all language versions) | A collection of treebanks in many languages. Used to train the agent on syntax, etymology, and translation, and to call linguistic analysis tools. |
| **`tanuki-historian`** | `Babelscape/wikineural` | A multilingual knowledge base. Used to train the agent to find and verify historical context relevant to literary works. |
| **`tanuki-cultural-analyst`** | `google-research-datasets/conceptual_captions` | Images with captions. Used to build a model of cultural concepts and how they are described, training the agent in cultural criticism. |
| **`tanuki-philosopher`** | `AlekseyKorshuk/logic-and-dialogue` & `servicenow/OpenOrca-Platypus` | Datasets focused on logic and reasoning. Used to train the agent on analyzing arguments, identifying fallacies, and discussing philosophical concepts. |
| **`tanuki-rhetorician`** | `iit-art-of-speech/iit-art-of-speech-v1` | A dataset of speeches with rhetorical analysis. Used to train the agent on identifying rhetorical devices and analyzing persuasive language. |
| **`tanuki-editor`** | `wikipedia` (specifically edit histories) & `un-yaml/C4_200M-token-stream` | Used to synthesize copy-editing tasks by treating the "edit" as the solution to a "problem" in the original text, teaching style and grammar correction. |

**Synthesis Example (`tanuki-literary-critic`):**
```python
def synthesize_literature_data(text_snippet_from_gutenberg):
    return {
        "instruction": "Analyze the provided text for its primary literary themes.",
        "thought": "I need to perform a close reading of this text, identify key motifs, and connect them to broader literary themes using my knowledge base.",
        "tool_calls": [
            {"tool": "thematic_analysis", "text": text_snippet_from_gutenberg},
            {"tool": "citation_format", "style": "mla"}
        ],
        "final_answer": "The primary theme of this text is..."
    }
```

### 3.2. System Overview
The architecture is a multi-stage agentic system designed for foresight, execution, and review.

```mermaid
graph TD
    A[Literary Query] --> B[Layer 1: Ingress & Sanitizer];
    B --> C[Layer 2: Foresight Agent (Planner-Critic)];
    C -- "Selects Optimal Plan" --> D[Layer 3: Orchestrator (Context Engineer)];
    
    subgraph "Layer 4: Execution & Adversarial Review"
        D -- "Routes to Expert" --> E(tanuki-literary-critic);
        E -- "Draft Analysis" --> F(tanuki-humanities-reviewer);
        F -- "Critique & Correction Request" --> E;
        F -- "Approved Analysis" --> G[Layer 5: Response Aggregator];
    end
    
    G --> H[Refined Literary Response];
```

### 3.3. Core Architectural Layers

| Layer | Component | Function |
|:---|:---|:---|
| 1 | **Ingress & Sanitizer** | Cleans user input and identifies the language. |
| 2 | **Foresight Agent** | Generates 2-3 high-level analytical plans (e.g., "Plan A: Focus on character archetypes. Plan B: Apply a post-structuralist lens.") and critiques them to select the most insightful path. |
| 3 | **Orchestrator Agent** | Assembles the "briefing packet" (full texts, critical essays, etc.) based on the selected plan and routes it to the appropriate expert. |
| 4 | **Execution & Review Loop** | An expert agent (`tanuki-literary-critic`) generates an analysis. This draft is immediately sent to an adversarial `tanuki-humanities-reviewer`, whose sole job is to find weak arguments or unsupported claims. If any are found, the analysis is sent back for refinement. |
| 5 | **Response Aggregator** | Formats the final, peer-reviewed analysis for the user. |

### 3.4. Leveraging Large Context for Advanced Literary Workflows

The 128k context window of our student model is the cornerstone of the Tanuki-Literature's effectiveness. It allows the Orchestrator Agent to provide the expert with a comprehensive "briefing packet" containing entire texts and critical analyses, enabling a depth of understanding previously impossible in small models.

**Example Briefing Packet for a Comparative Literature Task:**
```
<CONTEXT>
  <CONVERSATION_HISTORY>
    <!-- Full, unabridged user-AI dialogue about the analytical goal -->
  </CONVERSATION_HISTORY>

  <PRIMARY_TEXT_1>
    <!-- Full text of Shakespeare's "Hamlet" -->
  </PRIMARY_TEXT_1>
  
  <PRIMARY_TEXT_2>
    <!-- Full text of Sophocles' "Oedipus Rex" -->
  </PRIMARY_TEXT_2>

  <CRITICAL_ESSAY>
    <!-- Full text of a scholarly essay on tragic heroes -->
  </CRITICAL_ESSAY>
  
  <USER_QUERY>
    Compare and contrast the concept of the tragic flaw in Hamlet and Oedipus, using the provided critical essay as a theoretical framework.
  </USER_QUERY>
</CONTEXT>
```
This approach allows the expert agent to perform a true, deep comparative analysis by holding both primary texts and a secondary theoretical lens in its context simultaneously.

### 3.5. Specialized Tools Per Sub-Domain

| Sub-Domain | Tools & Resources |
|:---|:---|
| **Creative Writing** | Style analyzers, plot generators, character development tools |
| **Literary Analysis** | Close reading frameworks, thematic databases, literary theory guides |
| **Language Studies** | Etymology databases, linguistic corpora, translation tools |
| **Historical Research** | Digital archives, chronology tools, historical context databases |
| **Cultural Studies** | Cultural databases, anthropological frameworks, social context tools |
| **Philosophy** | Logical reasoning tools, argument analyzers, philosophical databases |
| **Rhetoric** | Rhetorical device catalogs, persuasion frameworks, speech analyzers |
| **Editorial** | Style guides (MLA, APA, Chicago), grammar checkers, publication standards |

---

## 4. Cultural Knowledge Architecture

### 4.1. Multi-Cultural Literary Database
```python
class CulturalKnowledgeEngine:
    def __init__(self):
        self.literary_traditions = load_world_literature_database()
        self.cultural_contexts = load_anthropological_database()
        self.historical_periods = load_historical_context_database()
        self.linguistic_families = load_language_family_database()
    
    def contextualize_analysis(self, text, cultural_context):
        """Provide culturally-aware literary analysis"""
        cultural_background = self.get_cultural_context(cultural_context)
        historical_period = self.identify_historical_period(text)
        literary_tradition = self.identify_tradition(text, cultural_context)
        return self.synthesize_cultural_analysis(text, cultural_background, 
                                               historical_period, literary_tradition)
```

### 4.2. Citation and Academic Integrity
- **Automatic Citation**: MLA, APA, Chicago style formatting
- **Plagiarism Detection**: Cross-reference with academic databases
- **Source Verification**: Academic credibility assessment
- **Attribution Tracking**: Proper credit for ideas and quotations

---

## 5. Resource Requirements & Performance

### 5.1. Memory Footprint & Quantization
The system is designed to run efficiently on consumer hardware by leveraging aggressive quantization.

- **Backbone Model**: Phi-3-mini-4K, quantized to **`Q4_K_M` using the GGUF format**. This is the key to fitting within the VRAM budget.
- **VRAM Usage**: ~2.4GB
- **8 LoRA Adapters**: ~720MB system RAM
- **Literary Databases**: ~3GB system RAM (cultural knowledge, references)
- **Language Models**: ~1GB system RAM (translation, linguistic analysis)
- **Total**: **2.4GB VRAM** + **~4.7GB system RAM**

### 5.2. Performance Targets
| Metric | Target | Benchmark |
|:---|:---|:---|
| **Creative Writing Quality** | 85% human preference | Blind evaluation studies |
| **Literary Analysis Depth** | 90% academic standards | Professor evaluation |
| **Translation Accuracy** | 92% BLEU score | Multi-language benchmarks |
| **Historical Accuracy** | 95% fact verification | Historical database cross-check |

---

## 6. Implementation Roadmap

### 6.1. Phase 1: Knowledge Infrastructure (Weeks 1-6)
- [ ] Build comprehensive literary and cultural databases
- [ ] Implement multi-language processing capabilities
- [ ] Create academic citation and reference systems
- [ ] Set up creative writing and analysis frameworks

### 6.2. Phase 2: Expert Training (Weeks 7-14)
- [ ] Generate synthetic training data for all humanities domains
- [ ] Train foundation LoRA adapters with cultural awareness
- [ ] Apply teacher-guided refinement for interpretive sophistication
- [ ] Benchmark against academic and creative writing standards

### 6.3. Phase 3: Advanced Features (Weeks 15-20)
- [ ] Implement collaborative writing and peer review features
- [ ] Add advanced rhetorical and stylistic analysis
- [ ] Create academic research and citation management
- [ ] Build creative writing workshop and feedback systems

---

## 7. Cost Analysis

### 7.1. Training Costs (for this Domain)
| Component | Cost | Notes |
|:---|:---|:---|
| **GPU Rental (Pro-rated)** | ~$7.50 | 1/4 of the shared $30 weekend rental. This budget covers all expert agents for the domain, including the planner and reviewer. |
| **Data Acquisition** | **$0** | All datasets are sourced for free from Hugging Face. |
| **Storage & Contingency** | ~$5 | Pro-rated from a shared $20 budget. |
| **Total** | **~$12.50** | Fully aligned with the ultra-low-cost budget of other domains. |

### 7.2. Competitive Advantages
- **vs. General Writing AIs**: Deep cultural and historical knowledge
- **vs. Academic Tools**: Integrated creative and analytical capabilities
- **vs. Translation Services**: Literary and cultural sensitivity
- **vs. Writing Assistants**: Sophisticated literary theory integration

---

## 8. Ethical Considerations & Cultural Sensitivity

### 8.1. Cultural Representation
- **Diverse Perspectives**: Inclusion of non-Western literary traditions
- **Cultural Sensitivity**: Respectful treatment of cultural differences
- **Bias Mitigation**: Active correction of cultural and literary biases
- **Indigenous Knowledge**: Respectful handling of indigenous literary traditions

### 8.2. Academic Integrity
- **Plagiarism Prevention**: Clear labeling of AI-generated content
- **Original Thought**: Encouragement of independent critical thinking
- **Source Attribution**: Proper academic citation and credit
- **Educational Support**: Enhancement rather than replacement of learning

### 8.3. Creative Rights
- **Authorship Transparency**: Clear indication of AI assistance in creative works
- **Style Imitation**: Ethical guidelines for mimicking existing authors
- **Copyright Respect**: Adherence to intellectual property laws
- **Creative Collaboration**: Framework for human-AI creative partnerships

---

*Domain: Language, Literature & Humanities | Target Users: Writers, Scholars, Students, Educators*
*Last Updated: January 2025 | Version: 1.0 | Status: Design Phase* 
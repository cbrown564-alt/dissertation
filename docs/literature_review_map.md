# Literature Review Map

This is a working map for the dissertation literature review. It prioritises direct publisher, PubMed/PMC, ACL Anthology, or arXiv links.

## Core Papers

| Theme | Paper | Relevance |
| --- | --- | --- |
| Synthetic seizure-frequency extraction | Gan et al., "Reproducible Synthetic Clinical Letters for Seizure Frequency Information Extraction", arXiv 2026. https://arxiv.org/abs/2603.11407 | Direct predecessor. Provides synthetic corpus, structured label scheme, evidence-grounded outputs, and fine-tuned model baseline. |
| KCL LLM epilepsy extraction | Fang et al., "Extracting epilepsy-related information from unstructured clinic letters using large language models", Epilepsia 2025. https://pmc.ncbi.nlm.nih.gov/articles/PMC12455391/ | KCL prior work on extracting epilepsy type, seizure type, current ASMs, and associated symptoms from 280 annotated KCH clinic letters. |
| KCL/BioNLP seizure-frequency LLM work | Holgate et al., "Extracting Epilepsy Patient Data with Llama 2", BioNLP 2024. https://aclanthology.org/2024.bionlp-1.43/ | Uses Llama 2 to extract seizure frequency from NHS EHR text; important direct comparator for prompt-based extraction. |
| Rule/statistical epilepsy extraction | Fonferko-Shadrach et al., "Using natural language processing to extract structured epilepsy data from unstructured clinic letters: development and validation of the ExECT system", BMJ Open 2019. https://pmc.ncbi.nlm.nih.gov/articles/PMC6500195/ | Earlier epilepsy clinic-letter extraction system. Uses GATE/Bio-YODIE and extracts nine epilepsy categories plus clinic date/date of birth. |
| Machine reading seizure-frequency extraction | Xie et al., "Extracting seizure frequency from epilepsy clinic notes", JAMIA 2022. https://pmc.ncbi.nlm.nih.gov/articles/PMC9006692/ | BERT/RoBERTa/Bio_ClinicalBERT question-answering approach for seizure freedom, frequency, and date of last seizure. |

## Review Threads

### Epilepsy Information Extraction

The dissertation should compare three generations of epilepsy NLP:

- Rule-based and hybrid clinical IE, represented by ExECT.
- Fine-tuned transformer and machine-reading systems, represented by Xie et al.
- Prompted and fine-tuned LLM systems, represented by Holgate et al., Fang et al., and Gan et al.

### Temporal Reasoning

Seizure frequency is harder than simple entity extraction because the answer is often a temporal calculation. The review should discuss:

- explicit rates: "two per week";
- retrospective windows: "four seizures over six months";
- seizure-free intervals: "seizure-free since June";
- cluster descriptions: "two cluster days per month, six seizures per cluster";
- stale or historical mentions that should not override current status;
- unknown or unsupported frequency.

### Synthetic Clinical Text

Gan et al. should be positioned as a privacy-preserving extension of clinical NLP methodology: synthetic letters allow open and reproducible development while avoiding distribution of real patient text. The literature review should still be careful not to overclaim external validity until real KCH evaluation is complete.

### Evidence-Grounded Outputs

The multi-agent framework should be justified around reliability:

- evidence spans make predictions auditable;
- verification catches unsupported or contradictory extractions;
- schema validation reduces downstream parsing failures;
- self-consistency can expose unstable outputs.

### Clinical Governance

Real patient data can only be used under approved governance. The paper should explicitly distinguish:

- synthetic development and evaluation in this repository;
- full synthetic corpus evaluation when provided;
- real KCH evaluation as a conditional later stage.

## Candidate Additional Literature To Add

- Clinical information extraction surveys.
- EHR de-identification and residual privacy risk.
- Synthetic clinical note generation and validation.
- Rationale/evidence evaluation in NLP.
- LLM-as-agent and multi-agent verification methods.
- Calibration and abstention in clinical AI.


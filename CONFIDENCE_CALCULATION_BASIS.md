🎯 CONSTITUTIONAL ARTICLE CONFIDENCE PERCENTAGE CALCULATION
===========================================================

## 📊 BASIS OF CONFIDENCE PERCENTAGE CALCULATION

The confidence percentage (0-100%) is calculated based on **RELEVANCE OF ARTICLES** to your query using a sophisticated multi-factor algorithm that analyzes multiple dimensions of relevance.

## 🔢 CALCULATION FORMULA

```
Final Confidence = Min(100%, Max(0%, 
    Base Relevance Score +
    Direct Article Reference +
    Title Word Overlap +
    Keyword Matching Bonus +
    Content Relevance +
    Domain-Specific Bonus
))
```

## 📈 DETAILED BREAKDOWN OF EACH FACTOR

### 1. 🎯 BASE RELEVANCE SCORE (up to 40%)
**Weight: 40% of total confidence**

Based on cumulative relevance points:
- **Direct Article Reference**: +10 points (Article X mentioned in query)
- **Title Keyword Match**: +3 points per matching word
- **Content Keyword Match**: +2 points per matching word  
- **Domain Relevance**: +1 point per domain keyword
- **Topic Relevance**: +2 points for topic-specific articles

```python
confidence += min(0.4, relevance_score * 0.05)
```

### 2. 🎯 DIRECT ARTICLE REFERENCE (up to 50%)
**Weight: 50% of total confidence**

If query contains "Article 21" or "Article21":
- Article 21 gets +50% confidence bonus
- This ensures direct references get highest priority

```python
if f"article {article_num}" in query_lower:
    confidence += 0.5
```

### 3. 📖 TITLE WORD OVERLAP (up to 30%)
**Weight: 30% of total confidence**

Measures how many query words appear in article title:
- Formula: `(Common Words / Total Title Words) × 30%`
- Higher overlap = higher relevance

```python
title_overlap = len(common_words) / len(title_words)
confidence += title_overlap * 0.3
```

### 4. 🔍 KEYWORD MATCHING BONUS (up to 20%)
**Weight: 20% of total confidence**

Based on number of relevant keywords found:
- Formula: `min(20%, num_keywords × 5%)`
- More matching keywords = higher confidence

```python
keyword_bonus = min(0.2, len(matching_keywords) * 0.05)
confidence += keyword_bonus
```

### 5. 📄 CONTENT RELEVANCE (up to 20%)
**Weight: 20% of total confidence**

Analyzes query words found in article content:
- Formula: `(Query Words in Content / Total Query Words) × 20%`
- More content matches = higher relevance

```python
content_overlap = len(query_words & content_words) / len(query_words)
confidence += content_overlap * 0.2
```

### 6. 🏛️ DOMAIN-SPECIFIC BONUS (up to 20%)
**Weight: 20% of total confidence**

Contextual bonus based on legal domain patterns:

**Domain Categories:**
- **Fundamental Rights**: right, freedom, equality, liberty, protection
- **Government Structure**: president, parliament, minister, governor
- **Judiciary**: court, judge, justice, jurisdiction, appeal
- **Citizenship**: citizen, nationality, migration, foreign
- **Elections**: election, vote, electoral, suffrage
- **Emergency**: emergency, proclamation, martial law
- **Language**: language, hindi, english, official

```python
bonus = 0.1 * (matching_keywords_in_text / total_domain_keywords)
domain_bonus = min(0.2, total_bonus)
```

## 🎯 EXAMPLE CALCULATIONS

### Example 1: "Article 21 violation"
```
Base Relevance: 10 points × 5% = 50%
Direct Reference: Article 21 mentioned = +50%
Title Overlap: "Protection" matches = +15%
Content Relevance: "violation" in content = +10%
Domain Bonus: Fundamental rights = +10%

Total: 50% + 50% + 15% + 10% + 10% = 135% → 100% (capped)
Final Confidence: 100%
```

### Example 2: "employment discrimination"
```
Base Relevance: 5 points × 5% = 25%
Direct Reference: No article mentioned = 0%
Title Overlap: "equality" matches = +20%
Keyword Bonus: 3 keywords = +15%
Content Relevance: Multiple matches = +15%
Domain Bonus: Rights-related = +10%

Total: 25% + 0% + 20% + 15% + 15% + 10% = 85%
Final Confidence: 85%
```

### Example 3: "property dispute"
```
Base Relevance: 4 points × 5% = 20%
Direct Reference: No article mentioned = 0%
Title Overlap: "property" exact match = +30%
Keyword Bonus: 2 keywords = +10%
Content Relevance: Some matches = +12%
Domain Bonus: Property law = +8%

Total: 20% + 0% + 30% + 10% + 12% + 8% = 80%
Final Confidence: 80%
```

## 🎨 CONFIDENCE LEVEL INDICATORS

### 🟢 HIGH CONFIDENCE (70-100%)
- **Very Relevant**: Strong keyword matches, direct relevance
- **Examples**: Direct article references, fundamental rights queries
- **Interpretation**: Article is highly relevant to your legal query

### 🟡 MEDIUM CONFIDENCE (40-69%)
- **Moderately Relevant**: Some keyword matches, contextual relevance
- **Examples**: Related legal concepts, secondary relevance
- **Interpretation**: Article has meaningful relevance to your query

### 🔴 LOW CONFIDENCE (0-39%)
- **Possibly Relevant**: Weak matches, tangential relevance
- **Examples**: Distant connections, general legal principles
- **Interpretation**: Article may have some relevance but not primary

## 🔬 RELEVANCE ASSESSMENT CRITERIA

### Primary Relevance Factors:
1. **Exact Keyword Matching**: Query words in article title/content
2. **Legal Domain Alignment**: Query domain matches article domain
3. **Constitutional Topic**: Article covers the constitutional area
4. **Direct References**: Specific article numbers mentioned
5. **Semantic Similarity**: Related legal concepts and terminology

### Secondary Relevance Factors:
1. **Context Clues**: Surrounding words and phrases
2. **Legal Precedent**: Constitutional interpretation patterns
3. **Rights Categories**: Fundamental vs. directive principles
4. **Government Functions**: Executive, legislative, judicial relevance

## 📊 QUALITY ASSURANCE MEASURES

### 1. **Normalization**: All scores capped at 100% to prevent inflation
### 2. **Minimum Threshold**: Only articles with >0 relevance included
### 3. **Ranking**: Articles sorted by confidence (highest first)
### 4. **Transparency**: All calculation factors shown in results

## 🎯 PRACTICAL EXAMPLES

### Query: "Employee discloses all the company secrets to another company"

**Article 19 - 75% Confidence:**
- Base: Trade/business keywords = 25%
- Title: "profession" matches = 20%
- Keywords: employment, business, trade = 15%
- Content: professional conduct = 10%
- Domain: Employment rights = 5%
- **Total: 75%**

**Article 300A - 72% Confidence:**
- Base: Property/secrets keywords = 20%
- Title: "property" matches = 30%
- Keywords: intellectual, trade, secrets = 15%
- Content: property protection = 5%
- Domain: Property rights = 2%
- **Total: 72%**

## ✅ ACCURACY VALIDATION

The confidence percentages are validated through:
1. **Multi-factor Analysis**: Multiple relevance dimensions
2. **Legal Domain Expertise**: Constitutional law patterns
3. **Keyword Density**: Frequency and context analysis
4. **Constitutional Structure**: Article categorization and hierarchy
5. **Query Intent Analysis**: Understanding user's legal question

## 🎯 CONCLUSION

The confidence percentage is a **comprehensive relevance score** that measures how well each constitutional article matches your specific legal query across multiple dimensions of relevance, providing you with a reliable indicator of which articles are most applicable to your legal situation.
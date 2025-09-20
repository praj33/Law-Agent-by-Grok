# 💬 Feedback Rating System - Quick Cheat Sheet

## 🚀 How to Start
```bash
python cli_interface.py                    # Standard mode
python cli_interface.py --adaptive        # Enhanced learning mode
```

## 📝 Basic Usage Flow

### 1. Ask a Legal Question
```
> my landlord is not returning my deposit
```

### 2. Give Feedback (Choose any method)

#### ✅ Simple Feedback (Just type the word)
```
> helpful
> not helpful
> good
> bad
> wrong
> excellent
> perfect
> thank you
```

#### ✅ Explicit Feedback (Using 'feedback' command)
```
> feedback helpful
> feedback not helpful
> feedback excellent
> feedback wrong domain
```

#### ✅ Natural Responses
```
> yes
> no
> correct
> right
> accurate
```

### 3. Continue Conversation
```
> what documents do I need?
> how long does this take?
> what are the next steps?
```

## 🧠 What Happens When You Give Feedback

| Feedback Type | Effect | Confidence Change |
|---------------|--------|-------------------|
| **Positive** (helpful, good, excellent) | ✅ Agent learns this works | +0.1 to +0.3 |
| **Negative** (not helpful, wrong, bad) | ❌ Agent learns to avoid this | -0.1 to -0.2 |

## 🔍 Debug Messages You'll See

```
🔍 Detected as QUERY: 'your legal question'
🧠 Detected as FEEDBACK: 'helpful'
📈 Confidence boost applied: +0.300
✅ Thank you! The agent has learned from your feedback.
```

## 💡 Pro Tips

### ✅ DO:
- Give feedback immediately after each response
- Use simple words: "helpful", "good", "bad"
- Ask follow-up questions after feedback
- Watch for debug messages

### ❌ DON'T:
- Give feedback without asking a question first
- Use very long sentences as feedback
- Mix feedback with new questions

## 🎯 Example Conversation

```
> my phone got stolen in market
🔍 Detected as QUERY: 'my phone got stolen in market'
[Agent provides criminal law advice]

> helpful
🧠 Detected as FEEDBACK: 'helpful'
✅ Thank you! The agent has learned from your feedback.

> what about filing a complaint
🔍 Detected as QUERY: 'what about filing a complaint'
[Agent provides complaint filing advice]

> good
🧠 Detected as FEEDBACK: 'good'
✅ Feedback processed, learning applied.
```

## 🔧 Other Commands

| Command | Purpose |
|---------|---------|
| `help` | Show help menu |
| `stats` | Show learning statistics |
| `clear` | Clear screen |
| `quit` | Exit the CLI |

## 🎉 That's It!

The agent learns and improves with every interaction. Just ask questions and give simple feedback!

# Demo Recording Guide — Learning Copilot

Instructions for recording a demo video for OpenAI App Review.

---

## OpenAI Requirements

- **Format:** Video (Loom / YouTube unlisted / Google Drive)
- **Duration:** 2–4 minutes is sufficient
- **Mode:** Developer Mode in ChatGPT

---

## About Learning Copilot

Learning Copilot helps users develop their role as a learner:

- **Assess learning stage** (from Random to Proactive)
- **Plan weekly learning rhythm** with pomodoros
- **Review progress** and track habits
- **Identify memes** — limiting beliefs that block learning

The Service is powered by an MCP server on Cloudflare Workers implementing a Finite State Machine (FSM).

---

## Recording Scenario

### 1. Preparation (do not record)

- Open ChatGPT in developer mode
- Connect the Learning Copilot app
- Make sure the MCP server is responding

### 2. Start Recording

#### Scene 1: Connection (30 sec)

Show:
- ChatGPT interface with the connected app
- The name "Learning Copilot" in the tools/actions list

#### Scene 2: Initial Greeting (30 sec)

**Request:** "Hello"
```
User: Hello
```

Show:
- Tool call: `get_instruction()` → returns `init` state
- Response with menu of available actions:
  - Review the week
  - Plan learning
  - Assess my stage
  - Set goals
  - Debug a blocker

Explain: "The assistant calls the MCP server and receives instructions for the current state"

#### Scene 3: Stage Assessment Flow (1–1.5 min)

**Request:** "Assess my learning stage"
```
User: Assess my learning stage
```

Show:
- Tool call: `get_instruction(state: "test_start")`
- Assistant asks diagnostic questions about learning habits

**User response:**
```
User: I try to study every day but often lose the rhythm after a week
```

Show:
- Tool call: `get_instruction(state: "assess_stage")`
- Result: "Your stage: Practicing"
- Explanation of criteria and recommendations for next level

#### Scene 4: Navigation Demo (30 sec)

**Request:** "Go back to start"
```
User: Go back to start
```

Show:
- Transition back to `init` state
- Menu appears again

Explain: "State transitions happen through explicit user actions. The FSM ensures predictable, structured dialogue."

#### Scene 5: Architecture Explanation (30 sec)

Explain by voice or text:
- "Each state has a specific purpose and defined transitions"
- "The MCP server returns instructions; the LLM follows them"
- "FSM architecture: state → instruction → response → next state"

### 3. Conclusion

- Show that the session ends correctly
- You can show the Developer console with tool calls

---

## Key Scenarios to Demonstrate

| Scenario | States Flow |
|----------|-------------|
| **Stage Assessment** | init → test_start → test_questions → assess_stage → assessment_result → init |
| **Weekly Planning** | init → plan_entry → plan_by_days → plan_invariants → plan_save → init |
| **Weekly Review** | init → weekly_reflection → weekly_reflection_save → next_week_planning → init |
| **Blocker Debug** | init → blocker_debug → meme_experiment → init |

---

## Learning Stages (for context)

| Stage | Timeframe | Key Indicator |
|-------|-----------|---------------|
| Random | — | No regular practice |
| Practicing | 1–2 weeks | Tries but loses rhythm |
| Systematic | 1–2 months | Stable rhythm |
| Disciplined | 3–6 months | Practice as habit |
| Proactive | 6+ months | Initiative and knowledge sharing |

---

## Where to Host the Video

| Platform | How to Do It |
|----------|--------------|
| **Loom** | Free, fast, public link |
| **YouTube (unlisted)** | "Unlisted" — access by link |
| **Google Drive** | Access "Anyone with the link" |
| **Cloudflare Stream** | If you have an account |

---

## Checklist Before Submitting

- [ ] Video shows Developer Mode
- [ ] Tool calls to MCP server are visible
- [ ] At least 2–3 different states are shown
- [ ] State transition logic is explained
- [ ] Video is accessible via public link
- [ ] Duration is 2–4 minutes

---

## Example Tool Calls (for demonstration)

**Initial state request:**
```json
{
  "name": "get_instruction",
  "arguments": {}
}
```

Response:
```json
{
  "state": "init",
  "instructions": "Greet the user and offer main actions...",
  "transitions": ["test_start", "plan_entry", "weekly_reflection", "blocker_debug"]
}
```

**Stage assessment request:**
```json
{
  "name": "get_instruction",
  "arguments": {
    "state": "assess_stage"
  }
}
```

Response:
```json
{
  "state": "assess_stage",
  "instructions": "Based on user responses, determine their learning stage...",
  "transitions": ["assessment_result", "init"]
}
```

---

## After Recording

1. Upload the video to your chosen platform
2. Copy the public link
3. Add the link to the OpenAI Apps form: **Demo Recording URL**
4. Update this document with the final link

---

## Demo Video Link

**URL:** `[Add after recording]`

---

**Last Updated:** January 2, 2025

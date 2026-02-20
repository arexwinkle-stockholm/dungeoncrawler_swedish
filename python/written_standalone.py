#!/usr/bin/env python3
"""
Build script to generate a standalone Dungeon Crawler HTML file
with all flashcard data embedded.

Usage: python scripts/build-standalone-dungeon.py
"""

import json
import os
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
FLASHCARD_DATA_PATH = "flashcard-data.json"
OUTPUT_PATH = "dungeon-crawler-standalone.html"


def load_flashcard_data():
    """Load flashcard data from JSON file."""
    with open(FLASHCARD_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def generate_html(flashcard_data):
    """Generate the complete standalone HTML with embedded data."""
    
    # Convert data to JSON string for embedding
    data_json = json.dumps(flashcard_data, ensure_ascii=False)
    
    html_template = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dungeon Crawler RPG - Swedish Vocabulary</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            min-height: 100vh;
            color: #e4e4e7;
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 1rem;
        }}
        
        .game-container {{
            max-width: 800px;
            width: 100%;
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .header h1 {{
            font-size: 1.5rem;
            background: linear-gradient(135deg, #f59e0b, #ef4444);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 0.25rem;
        }}
        
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 1rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
            padding: 0.75rem;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 0.5rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .stat {{
            display: flex;
            align-items: center;
            gap: 0.25rem;
            font-size: 0.875rem;
        }}
        
        .stat-icon {{
            font-size: 1rem;
        }}
        
        .hp-bar {{
            width: 100px;
            height: 8px;
            background: #374151;
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .hp-fill {{
            height: 100%;
            background: linear-gradient(90deg, #ef4444, #22c55e);
            transition: width 0.3s ease;
        }}
        
        .dungeon-container {{
            background: rgba(0, 0, 0, 0.4);
            border-radius: 0.75rem;
            padding: 1rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-bottom: 1rem;
        }}
        
        .floor-info {{
            text-align: center;
            margin-bottom: 0.75rem;
            font-size: 0.875rem;
            color: #a1a1aa;
        }}
        
        .dungeon-grid {{
            display: grid;
            gap: 2px;
            justify-content: center;
            margin-bottom: 1rem;
        }}
        
        .cell {{
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            border-radius: 4px;
            transition: all 0.2s ease;
        }}
        
        .cell-wall {{
            background: #1f2937;
        }}
        
        .cell-floor {{
            background: #374151;
        }}
        
        .cell-fog {{
            background: #111827;
        }}
        
        .cell-player {{
            background: #3b82f6;
            box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
        }}
        
        .cell-monster {{
            background: #7c3aed;
            animation: pulse 2s infinite;
        }}
        
        .cell-stairs {{
            background: #f59e0b;
        }}
        
        .cell-chest {{
            background: #eab308;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.7; }}
        }}
        
        .controls {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .control-row {{
            display: flex;
            gap: 0.25rem;
        }}
        
        .control-btn {{
            width: 50px;
            height: 50px;
            font-size: 1.25rem;
            border: none;
            border-radius: 0.5rem;
            background: linear-gradient(135deg, #4b5563, #374151);
            color: white;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s ease;
            touch-action: manipulation;
        }}
        
        .control-btn:hover {{
            background: linear-gradient(135deg, #6b7280, #4b5563);
            transform: scale(1.05);
        }}
        
        .control-btn:active {{
            transform: scale(0.95);
        }}
        
        .control-placeholder {{
            width: 50px;
            height: 50px;
        }}
        
        .message-log {{
            background: rgba(0, 0, 0, 0.3);
            border-radius: 0.5rem;
            padding: 0.75rem;
            max-height: 100px;
            overflow-y: auto;
            font-size: 0.75rem;
            border: 1px solid rgba(255, 255, 255, 0.1);
        }}
        
        .message {{
            padding: 0.25rem 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }}
        
        .message:last-child {{
            border-bottom: none;
        }}
        
        .message-combat {{
            color: #f87171;
        }}
        
        .message-reward {{
            color: #fbbf24;
        }}
        
        .message-info {{
            color: #60a5fa;
        }}
        
        /* Combat Modal */
        .modal-overlay {{
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0, 0, 0, 0.8);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
            padding: 1rem;
        }}
        
        .modal-hidden {{
            display: none;
        }}
        
        .combat-modal {{
            background: linear-gradient(135deg, #1e1b4b, #312e81);
            border-radius: 1rem;
            padding: 1.5rem;
            max-width: 500px;
            width: 100%;
            border: 2px solid #6366f1;
            box-shadow: 0 0 30px rgba(99, 102, 241, 0.3);
        }}
        
        .combat-header {{
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .monster-name {{
            font-size: 1.25rem;
            color: #c4b5fd;
            margin-bottom: 0.25rem;
        }}
        
        .monster-hp {{
            font-size: 0.875rem;
            color: #a1a1aa;
        }}
        
        .flashcard {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 0.75rem;
            padding: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .flashcard-prompt {{
            font-size: 0.75rem;
            color: #a1a1aa;
            margin-bottom: 0.5rem;
        }}
        
        .flashcard-word {{
            font-size: 1.5rem;
            font-weight: bold;
            color: #e4e4e7;
        }}
        
        .answer-input {{
            width: 100%;
            padding: 0.75rem;
            font-size: 1rem;
            border: 2px solid #4b5563;
            border-radius: 0.5rem;
            background: rgba(0, 0, 0, 0.3);
            color: white;
            margin-bottom: 0.75rem;
            text-align: center;
        }}
        
        .answer-input:focus {{
            outline: none;
            border-color: #6366f1;
        }}
        
        .combat-buttons {{
            display: flex;
            gap: 0.5rem;
        }}
        
        .combat-btn {{
            flex: 1;
            padding: 0.75rem;
            font-size: 1rem;
            border: none;
            border-radius: 0.5rem;
            cursor: pointer;
            font-weight: bold;
            transition: all 0.2s ease;
        }}
        
        .btn-attack {{
            background: linear-gradient(135deg, #dc2626, #b91c1c);
            color: white;
        }}
        
        .btn-attack:hover {{
            transform: scale(1.02);
        }}
        
        .btn-flee {{
            background: linear-gradient(135deg, #4b5563, #374151);
            color: white;
        }}
        
        .combat-result {{
            text-align: center;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-top: 0.75rem;
            font-weight: bold;
        }}
        
        .result-correct {{
            background: rgba(34, 197, 94, 0.2);
            color: #4ade80;
        }}
        
        .result-incorrect {{
            background: rgba(239, 68, 68, 0.2);
            color: #f87171;
        }}
        
        .streak-display {{
            text-align: center;
            margin-bottom: 0.5rem;
            font-size: 0.875rem;
        }}
        
        .streak-fire {{
            color: #f59e0b;
        }}
        
        /* Game Over / Victory Modal */
        .game-over-modal {{
            background: linear-gradient(135deg, #450a0a, #7f1d1d);
            border-color: #dc2626;
        }}
        
        .victory-modal {{
            background: linear-gradient(135deg, #14532d, #166534);
            border-color: #22c55e;
        }}
        
        .modal-title {{
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 1rem;
        }}
        
        .modal-text {{
            text-align: center;
            margin-bottom: 1rem;
            color: #a1a1aa;
        }}
        
        .restart-btn {{
            width: 100%;
            padding: 1rem;
            font-size: 1rem;
            border: none;
            border-radius: 0.5rem;
            background: linear-gradient(135deg, #6366f1, #4f46e5);
            color: white;
            cursor: pointer;
            font-weight: bold;
        }}
        
        .instructions {{
            margin-top: 1rem;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.2);
            border-radius: 0.5rem;
            font-size: 0.75rem;
            color: #a1a1aa;
        }}
        
        .instructions h3 {{
            color: #e4e4e7;
            margin-bottom: 0.5rem;
        }}
        
        .instructions ul {{
            list-style: none;
            padding: 0;
        }}
        
        .instructions li {{
            padding: 0.25rem 0;
        }}
        
        @media (max-width: 480px) {{
            .cell {{
                width: 22px;
                height: 22px;
                font-size: 12px;
            }}
            
            .control-btn {{
                width: 60px;
                height: 60px;
            }}
            
            .control-placeholder {{
                width: 60px;
                height: 60px;
            }}
        }}
    </style>
</head>
<body>
    <div class="game-container">
        <div class="header">
            <h1>🏰 Dungeon Crawler RPG</h1>
            <p style="font-size: 0.75rem; color: #a1a1aa;">Learn Swedish by battling monsters!</p>
        </div>
        
        <div class="stats-bar">
            <div class="stat">
                <span class="stat-icon">❤️</span>
                <div class="hp-bar">
                    <div class="hp-fill" id="hp-bar"></div>
                </div>
                <span id="hp-text">100/100</span>
            </div>
            <div class="stat">
                <span class="stat-icon">⭐</span>
                <span>Lv. <span id="level">1</span></span>
            </div>
            <div class="stat">
                <span class="stat-icon">✨</span>
                <span><span id="xp">0</span>/<span id="xp-needed">100</span></span>
            </div>
            <div class="stat">
                <span class="stat-icon">💰</span>
                <span id="gold">0</span>
            </div>
        </div>
        
        <div class="dungeon-container">
            <div class="floor-info">
                Floor <span id="floor">1</span> | Chapter: <span id="chapter">1</span>
            </div>
            <div class="dungeon-grid" id="dungeon-grid"></div>
            <div class="controls">
                <div class="control-row">
                    <div class="control-placeholder"></div>
                    <button class="control-btn" onclick="movePlayer(0, -1)">⬆️</button>
                    <div class="control-placeholder"></div>
                </div>
                <div class="control-row">
                    <button class="control-btn" onclick="movePlayer(-1, 0)">⬅️</button>
                    <button class="control-btn" onclick="movePlayer(0, 1)">⬇️</button>
                    <button class="control-btn" onclick="movePlayer(1, 0)">➡️</button>
                </div>
            </div>
        </div>
        
        <div class="message-log" id="message-log"></div>
        
        <div class="instructions">
            <h3>How to Play</h3>
            <ul>
                <li>🎮 Use arrow keys or buttons to move</li>
                <li>👾 Encounter monsters and answer vocabulary questions</li>
                <li>⚔️ Correct answers deal damage, wrong answers hurt you</li>
                <li>🔥 Build streaks for bonus damage</li>
                <li>🪜 Find stairs to go deeper</li>
            </ul>
        </div>
    </div>
    
    <!-- Combat Modal -->
    <div class="modal-overlay modal-hidden" id="combat-modal">
        <div class="combat-modal">
            <div class="combat-header">
                <div class="monster-name" id="monster-name">👾 Monster</div>
                <div class="monster-hp">HP: <span id="monster-hp">50</span>/<span id="monster-max-hp">50</span></div>
            </div>
            <div class="streak-display" id="streak-display"></div>
            <div class="flashcard">
                <div class="flashcard-prompt">Translate to English:</div>
                <div class="flashcard-word" id="flashcard-word">svenska</div>
            </div>
            <input type="text" class="answer-input" id="answer-input" placeholder="Type your answer..." autocomplete="off">
            <div class="combat-buttons">
                <button class="combat-btn btn-attack" onclick="submitAnswer()">⚔️ Attack</button>
                <button class="combat-btn btn-flee" onclick="fleeCombat()">🏃 Flee</button>
            </div>
            <div class="combat-result modal-hidden" id="combat-result"></div>
        </div>
    </div>
    
    <!-- Game Over Modal -->
    <div class="modal-overlay modal-hidden" id="gameover-modal">
        <div class="combat-modal game-over-modal">
            <div class="modal-title">💀 Game Over</div>
            <div class="modal-text">You were defeated on Floor <span id="final-floor">1</span></div>
            <button class="restart-btn" onclick="restartGame()">🔄 Try Again</button>
        </div>
    </div>

    <script>
        // ============================================
        // FLASHCARD DATA (Auto-injected by build script)
        // ============================================
        const RAW_FLASHCARD_DATA = {data_json};
        
        // Process data into chapter-based structure
        function processFlashcardData(rawData) {{
            const chapters = {{}};
            rawData.forEach(card => {{
                const chapter = card.chapter || 'Chapter1';
                if (!chapters[chapter]) {{
                    chapters[chapter] = [];
                }}
                chapters[chapter].push({{
                    front: card.front,
                    back: card.back
                }});
            }});
            return chapters;
        }}
        
        const FLASHCARD_DATA = processFlashcardData(RAW_FLASHCARD_DATA);
        const AVAILABLE_CHAPTERS = Object.keys(FLASHCARD_DATA).sort();
        
        // ============================================
        // GAME STATE
        // ============================================
        let gameState = {{
            player: {{ x: 1, y: 1, hp: 100, maxHp: 100, level: 1, xp: 0, gold: 0 }},
            floor: 1,
            currentChapter: AVAILABLE_CHAPTERS[0] || 'Chapter1',
            dungeon: [],
            monsters: [],
            stairs: null,
            revealed: new Set(),
            streak: 0,
            messages: [],
            inCombat: false,
            currentMonster: null,
            currentCard: null
        }};
        
        const GRID_SIZE = 15;
        const VISION_RADIUS = 3;
        
        const MONSTER_TYPES = [
            {{ name: 'Slime', emoji: '🟢', hp: 30, damage: 5, xp: 15, gold: 5 }},
            {{ name: 'Goblin', emoji: '👺', hp: 40, damage: 8, xp: 25, gold: 10 }},
            {{ name: 'Skeleton', emoji: '💀', hp: 50, damage: 10, xp: 35, gold: 15 }},
            {{ name: 'Ghost', emoji: '👻', hp: 35, damage: 12, xp: 40, gold: 20 }},
            {{ name: 'Orc', emoji: '👹', hp: 70, damage: 15, xp: 50, gold: 25 }},
            {{ name: 'Dragon', emoji: '🐉', hp: 100, damage: 20, xp: 100, gold: 50 }}
        ];
        
        // ============================================
        // DUNGEON GENERATION
        // ============================================
        function generateDungeon() {{
            // Initialize with walls
            const dungeon = Array(GRID_SIZE).fill(null).map(() => 
                Array(GRID_SIZE).fill('wall')
            );
            
            // Generate rooms
            const rooms = [];
            const numRooms = 4 + Math.floor(Math.random() * 3);
            
            for (let i = 0; i < numRooms; i++) {{
                const roomWidth = 3 + Math.floor(Math.random() * 4);
                const roomHeight = 3 + Math.floor(Math.random() * 4);
                const roomX = 1 + Math.floor(Math.random() * (GRID_SIZE - roomWidth - 2));
                const roomY = 1 + Math.floor(Math.random() * (GRID_SIZE - roomHeight - 2));
                
                // Check for overlap
                let overlaps = false;
                for (const room of rooms) {{
                    if (roomX < room.x + room.width + 1 && 
                        roomX + roomWidth + 1 > room.x &&
                        roomY < room.y + room.height + 1 && 
                        roomY + roomHeight + 1 > room.y) {{
                        overlaps = true;
                        break;
                    }}
                }}
                
                if (!overlaps) {{
                    rooms.push({{ x: roomX, y: roomY, width: roomWidth, height: roomHeight }});
                    
                    // Carve room
                    for (let x = roomX; x < roomX + roomWidth; x++) {{
                        for (let y = roomY; y < roomY + roomHeight; y++) {{
                            dungeon[y][x] = 'floor';
                        }}
                    }}
                }}
            }}
            
            // Connect rooms with corridors
            for (let i = 1; i < rooms.length; i++) {{
                const room1 = rooms[i - 1];
                const room2 = rooms[i];
                
                const x1 = Math.floor(room1.x + room1.width / 2);
                const y1 = Math.floor(room1.y + room1.height / 2);
                const x2 = Math.floor(room2.x + room2.width / 2);
                const y2 = Math.floor(room2.y + room2.height / 2);
                
                // Horizontal then vertical
                let x = x1;
                while (x !== x2) {{
                    dungeon[y1][x] = 'floor';
                    x += x2 > x1 ? 1 : -1;
                }}
                let y = y1;
                while (y !== y2) {{
                    dungeon[y][x2] = 'floor';
                    y += y2 > y1 ? 1 : -1;
                }}
            }}
            
            return {{ dungeon, rooms }};
        }}
        
        function getFloorCells(dungeon) {{
            const cells = [];
            for (let y = 0; y < GRID_SIZE; y++) {{
                for (let x = 0; x < GRID_SIZE; x++) {{
                    if (dungeon[y][x] === 'floor') {{
                        cells.push({{ x, y }});
                    }}
                }}
            }}
            return cells;
        }}
        
        function initFloor() {{
            const {{ dungeon, rooms }} = generateDungeon();
            gameState.dungeon = dungeon;
            gameState.revealed = new Set();
            
            const floorCells = getFloorCells(dungeon);
            
            // Place player in first room
            if (rooms.length > 0) {{
                gameState.player.x = rooms[0].x + 1;
                gameState.player.y = rooms[0].y + 1;
            }} else {{
                const startCell = floorCells[0];
                gameState.player.x = startCell.x;
                gameState.player.y = startCell.y;
            }}
            
            // Remove player position from available cells
            const availableCells = floorCells.filter(c => 
                !(c.x === gameState.player.x && c.y === gameState.player.y)
            );
            
            // Place stairs in last room
            if (rooms.length > 1) {{
                const lastRoom = rooms[rooms.length - 1];
                gameState.stairs = {{ 
                    x: lastRoom.x + Math.floor(lastRoom.width / 2), 
                    y: lastRoom.y + Math.floor(lastRoom.height / 2) 
                }};
            }} else {{
                const stairCell = availableCells[availableCells.length - 1];
                gameState.stairs = {{ x: stairCell.x, y: stairCell.y }};
            }}
            
            // Place monsters
            const numMonsters = 3 + gameState.floor;
            gameState.monsters = [];
            
            const monsterCells = availableCells.filter(c => 
                !(c.x === gameState.stairs.x && c.y === gameState.stairs.y)
            );
            
            for (let i = 0; i < Math.min(numMonsters, monsterCells.length); i++) {{
                const idx = Math.floor(Math.random() * monsterCells.length);
                const cell = monsterCells.splice(idx, 1)[0];
                
                // Higher floors get tougher monsters
                const maxMonsterIdx = Math.min(gameState.floor, MONSTER_TYPES.length - 1);
                const monsterIdx = Math.floor(Math.random() * (maxMonsterIdx + 1));
                const monsterType = MONSTER_TYPES[monsterIdx];
                
                // Scale monster stats with floor
                const floorScale = 1 + (gameState.floor - 1) * 0.2;
                
                gameState.monsters.push({{
                    ...monsterType,
                    x: cell.x,
                    y: cell.y,
                    hp: Math.floor(monsterType.hp * floorScale),
                    maxHp: Math.floor(monsterType.hp * floorScale),
                    damage: Math.floor(monsterType.damage * floorScale)
                }});
            }}
            
            // Update chapter based on floor
            const chapterIdx = (gameState.floor - 1) % AVAILABLE_CHAPTERS.length;
            gameState.currentChapter = AVAILABLE_CHAPTERS[chapterIdx];
            
            updateVision();
            render();
            addMessage(`Entered Floor ${{gameState.floor}} - Chapter: ${{gameState.currentChapter}}`, 'info');
        }}
        
        function updateVision() {{
            const {{ x: px, y: py }} = gameState.player;
            
            for (let dy = -VISION_RADIUS; dy <= VISION_RADIUS; dy++) {{
                for (let dx = -VISION_RADIUS; dx <= VISION_RADIUS; dx++) {{
                    const x = px + dx;
                    const y = py + dy;
                    
                    if (x >= 0 && x < GRID_SIZE && y >= 0 && y < GRID_SIZE) {{
                        const dist = Math.sqrt(dx * dx + dy * dy);
                        if (dist <= VISION_RADIUS) {{
                            gameState.revealed.add(`${{x}},${{y}}`);
                        }}
                    }}
                }}
            }}
        }}
        
        // ============================================
        // RENDERING
        // ============================================
        function render() {{
            const grid = document.getElementById('dungeon-grid');
            grid.style.gridTemplateColumns = `repeat(${{GRID_SIZE}}, 28px)`;
            grid.innerHTML = '';
            
            for (let y = 0; y < GRID_SIZE; y++) {{
                for (let x = 0; x < GRID_SIZE; x++) {{
                    const cell = document.createElement('div');
                    cell.className = 'cell';
                    
                    const key = `${{x}},${{y}}`;
                    const isRevealed = gameState.revealed.has(key);
                    
                    if (!isRevealed) {{
                        cell.classList.add('cell-fog');
                    }} else if (x === gameState.player.x && y === gameState.player.y) {{
                        cell.classList.add('cell-player');
                        cell.textContent = '🧙';
                    }} else if (gameState.stairs && x === gameState.stairs.x && y === gameState.stairs.y) {{
                        cell.classList.add('cell-stairs');
                        cell.textContent = '🪜';
                    }} else {{
                        const monster = gameState.monsters.find(m => m.x === x && m.y === y);
                        if (monster) {{
                            cell.classList.add('cell-monster');
                            cell.textContent = monster.emoji;
                        }} else if (gameState.dungeon[y][x] === 'wall') {{
                            cell.classList.add('cell-wall');
                        }} else {{
                            cell.classList.add('cell-floor');
                        }}
                    }}
                    
                    grid.appendChild(cell);
                }}
            }}
            
            // Update stats
            const hpPercent = (gameState.player.hp / gameState.player.maxHp) * 100;
            document.getElementById('hp-bar').style.width = `${{hpPercent}}%`;
            document.getElementById('hp-text').textContent = `${{gameState.player.hp}}/${{gameState.player.maxHp}}`;
            document.getElementById('level').textContent = gameState.player.level;
            document.getElementById('xp').textContent = gameState.player.xp;
            document.getElementById('xp-needed').textContent = getXpForNextLevel();
            document.getElementById('gold').textContent = gameState.player.gold;
            document.getElementById('floor').textContent = gameState.floor;
            document.getElementById('chapter').textContent = gameState.currentChapter.replace('Chapter', '');
        }}
        
        function getXpForNextLevel() {{
            return gameState.player.level * 100;
        }}
        
        function addMessage(text, type = 'info') {{
            gameState.messages.unshift({{ text, type }});
            if (gameState.messages.length > 20) gameState.messages.pop();
            
            const log = document.getElementById('message-log');
            log.innerHTML = gameState.messages.map(m => 
                `<div class="message message-${{m.type}}">${{m.text}}</div>`
            ).join('');
        }}
        
        // ============================================
        // MOVEMENT
        // ============================================
        function movePlayer(dx, dy) {{
            if (gameState.inCombat) return;
            
            const newX = gameState.player.x + dx;
            const newY = gameState.player.y + dy;
            
            // Bounds check
            if (newX < 0 || newX >= GRID_SIZE || newY < 0 || newY >= GRID_SIZE) return;
            
            // Wall check
            if (gameState.dungeon[newY][newX] === 'wall') return;
            
            // Monster check
            const monster = gameState.monsters.find(m => m.x === newX && m.y === newY);
            if (monster) {{
                startCombat(monster);
                return;
            }}
            
            // Move player
            gameState.player.x = newX;
            gameState.player.y = newY;
            
            // Stairs check
            if (gameState.stairs && newX === gameState.stairs.x && newY === gameState.stairs.y) {{
                gameState.floor++;
                addMessage(`Descending to Floor ${{gameState.floor}}...`, 'info');
                initFloor();
                return;
            }}
            
            updateVision();
            render();
        }}
        
        // Keyboard controls
        document.addEventListener('keydown', (e) => {{
            switch(e.key) {{
                case 'ArrowUp':
                case 'w':
                case 'W':
                    movePlayer(0, -1);
                    break;
                case 'ArrowDown':
                case 's':
                case 'S':
                    movePlayer(0, 1);
                    break;
                case 'ArrowLeft':
                case 'a':
                case 'A':
                    movePlayer(-1, 0);
                    break;
                case 'ArrowRight':
                case 'd':
                case 'D':
                    movePlayer(1, 0);
                    break;
            }}
        }});
        
        // ============================================
        // COMBAT
        // ============================================
        function getRandomCard() {{
            const cards = FLASHCARD_DATA[gameState.currentChapter] || FLASHCARD_DATA[AVAILABLE_CHAPTERS[0]];
            if (!cards || cards.length === 0) return {{ front: 'hej', back: 'hello' }};
            return cards[Math.floor(Math.random() * cards.length)];
        }}
        
        function startCombat(monster) {{
            gameState.inCombat = true;
            gameState.currentMonster = monster;
            gameState.currentCard = getRandomCard();
            
            document.getElementById('monster-name').textContent = `${{monster.emoji}} ${{monster.name}}`;
            document.getElementById('monster-hp').textContent = monster.hp;
            document.getElementById('monster-max-hp').textContent = monster.maxHp;
            document.getElementById('flashcard-word').textContent = gameState.currentCard.front;
            document.getElementById('answer-input').value = '';
            document.getElementById('combat-result').classList.add('modal-hidden');
            
            updateStreakDisplay();
            
            document.getElementById('combat-modal').classList.remove('modal-hidden');
            document.getElementById('answer-input').focus();
        }}
        
        function updateStreakDisplay() {{
            const display = document.getElementById('streak-display');
            if (gameState.streak > 0) {{
                display.innerHTML = `<span class="streak-fire">🔥 Streak: ${{gameState.streak}} (x${{1 + gameState.streak * 0.5}} damage)</span>`;
            }} else {{
                display.innerHTML = '';
            }}
        }}
        
        function normalizeAnswer(str) {{
            return str.toLowerCase().trim()
                .replace(/[.,!?;:'"()\\[\\]{{}}]/g, '')
                .replace(/\\s+/g, ' ');
        }}
        
        function checkAnswer(userAnswer, correctAnswer) {{
            const normalizedUser = normalizeAnswer(userAnswer);
            const normalizedCorrect = normalizeAnswer(correctAnswer);
            
            // Exact match
            if (normalizedUser === normalizedCorrect) return true;
            
            // Check if answer contains the correct one (for multi-word translations)
            const correctWords = normalizedCorrect.split(/[,\\/]/).map(s => s.trim());
            return correctWords.some(word => normalizeAnswer(word) === normalizedUser);
        }}
        
        function submitAnswer() {{
            const input = document.getElementById('answer-input');
            const userAnswer = input.value;
            const correct = checkAnswer(userAnswer, gameState.currentCard.back);
            
            const resultDiv = document.getElementById('combat-result');
            resultDiv.classList.remove('modal-hidden', 'result-correct', 'result-incorrect');
            
            if (correct) {{
                gameState.streak++;
                const damageMultiplier = 1 + gameState.streak * 0.5;
                const baseDamage = 10 + gameState.player.level * 5;
                const damage = Math.floor(baseDamage * damageMultiplier);
                
                gameState.currentMonster.hp -= damage;
                
                resultDiv.classList.add('result-correct');
                resultDiv.textContent = `✅ Correct! Dealt ${{damage}} damage!`;
                
                document.getElementById('monster-hp').textContent = Math.max(0, gameState.currentMonster.hp);
                
                if (gameState.currentMonster.hp <= 0) {{
                    // Monster defeated
                    setTimeout(() => defeatMonster(), 1000);
                }} else {{
                    // Continue combat with new card
                    setTimeout(() => {{
                        gameState.currentCard = getRandomCard();
                        document.getElementById('flashcard-word').textContent = gameState.currentCard.front;
                        input.value = '';
                        resultDiv.classList.add('modal-hidden');
                        updateStreakDisplay();
                        input.focus();
                    }}, 1000);
                }}
            }} else {{
                gameState.streak = 0;
                const damage = gameState.currentMonster.damage;
                gameState.player.hp -= damage;
                
                resultDiv.classList.add('result-incorrect');
                resultDiv.textContent = `❌ Wrong! The answer was "${{gameState.currentCard.back}}". You took ${{damage}} damage!`;
                
                if (gameState.player.hp <= 0) {{
                    setTimeout(() => gameOver(), 1000);
                }} else {{
                    setTimeout(() => {{
                        gameState.currentCard = getRandomCard();
                        document.getElementById('flashcard-word').textContent = gameState.currentCard.front;
                        input.value = '';
                        resultDiv.classList.add('modal-hidden');
                        updateStreakDisplay();
                        render();
                        input.focus();
                    }}, 1500);
                }}
            }}
        }}
        
        function defeatMonster() {{
            const monster = gameState.currentMonster;
            
            // Award XP and gold
            gameState.player.xp += monster.xp;
            gameState.player.gold += monster.gold;
            
            addMessage(`Defeated ${{monster.name}}! +${{monster.xp}} XP, +${{monster.gold}} gold`, 'reward');
            
            // Remove monster
            gameState.monsters = gameState.monsters.filter(m => m !== monster);
            
            // Check level up
            while (gameState.player.xp >= getXpForNextLevel()) {{
                gameState.player.xp -= getXpForNextLevel();
                gameState.player.level++;
                gameState.player.maxHp += 20;
                gameState.player.hp = gameState.player.maxHp;
                addMessage(`🎉 Level Up! Now level ${{gameState.player.level}}!`, 'reward');
            }}
            
            endCombat();
        }}
        
        function fleeCombat() {{
            gameState.streak = 0;
            const damage = Math.floor(gameState.currentMonster.damage / 2);
            gameState.player.hp -= damage;
            
            addMessage(`Fled from ${{gameState.currentMonster.name}}! Took ${{damage}} damage.`, 'combat');
            
            if (gameState.player.hp <= 0) {{
                gameOver();
            }} else {{
                endCombat();
            }}
        }}
        
        function endCombat() {{
            gameState.inCombat = false;
            gameState.currentMonster = null;
            gameState.currentCard = null;
            
            document.getElementById('combat-modal').classList.add('modal-hidden');
            render();
        }}
        
        function gameOver() {{
            document.getElementById('combat-modal').classList.add('modal-hidden');
            document.getElementById('final-floor').textContent = gameState.floor;
            document.getElementById('gameover-modal').classList.remove('modal-hidden');
        }}
        
        function restartGame() {{
            gameState = {{
                player: {{ x: 1, y: 1, hp: 100, maxHp: 100, level: 1, xp: 0, gold: 0 }},
                floor: 1,
                currentChapter: AVAILABLE_CHAPTERS[0] || 'Chapter1',
                dungeon: [],
                monsters: [],
                stairs: null,
                revealed: new Set(),
                streak: 0,
                messages: [],
                inCombat: false,
                currentMonster: null,
                currentCard: null
            }};
            
            document.getElementById('gameover-modal').classList.add('modal-hidden');
            initFloor();
        }}
        
        // Handle Enter key in combat
        document.getElementById('answer-input').addEventListener('keydown', (e) => {{
            if (e.key === 'Enter') {{
                submitAnswer();
            }}
        }});
        
        // ============================================
        // START GAME
        // ============================================
        initFloor();
        addMessage('Welcome to the dungeon! Find the stairs to descend.', 'info');
    </script>
</body>
</html>'''
    
    return html_template


def main():
    """Main build function."""
    print("🏰 Building Dungeon Crawler Standalone HTML...")
    
    # Load flashcard data
    print(f"📖 Loading flashcard data from {FLASHCARD_DATA_PATH}...")
    flashcard_data = load_flashcard_data()
    print(f"   Found {len(flashcard_data)} flashcards")
    
    # Count chapters
    chapters = set(card.get('chapter', 'Chapter1') for card in flashcard_data)
    print(f"   Chapters: {sorted(chapters)}")
    
    # Generate HTML
    print("🔨 Generating standalone HTML...")
    html_content = generate_html(flashcard_data)
    
    # Write output
    print(f"💾 Writing to {OUTPUT_PATH}...")
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Report file size
    file_size = os.path.getsize(OUTPUT_PATH)
    print(f"✅ Done! File size: {file_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()

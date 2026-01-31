# o que é uma “boa posição” em EGGS?
🥚 Princípios estratégicos reais do jogo (extraídos das regras)

1️⃣ Avançar com estabilidade > avançar rápido
Chegar na última fileira sem tensão é vitória.
Logo:
avanço protegido > avanço isolado
👉 IA deve preferir:
- cadeias
- peças que não podem ser comidas


2️⃣ Colunas são fortes porque reduzem vetores de ataque
Em tabuleiros maiores:
- colunas continuam importantes
- mas o centro ganha valor relativo


3️⃣ Conter é mais importante que capturar
Captura é obrigatória → pode ser armadilha.
Boa posição:
- força captura ruim
- cria zugzwang
- trava cadeias
Isso é difícil de avaliar automaticamente — minimax faz isso melhor que heurística.


4️⃣ Peça a mais geralmente decide
Especialmente com poucas peças.
Com mais peças?
- talvez surjam sacrifícios posicionais
- mas isso só aparece em tabuleiros maiores
Por enquanto:
✔️ material alto = vitória provável



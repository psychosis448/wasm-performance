export const drawMaze = ({ maze, ctx, scale, width, height, cellWidth, offset }) => {
    ctx.scale(scale, scale);
    ctx.fillRect(0, 0, width, height);

    ctx.strokeStyle = "white";
    ctx.lineWidth = offset;
    ctx.lineCap = "square";

    maze.forEach((value, key) => {
        const [keyX, keyY] = key.split(",");
        const fromX = keyX * cellWidth + 1;
        const fromY = keyY * cellWidth + 1;

        value.forEach((to) => {
            const [xA, yA] = to.split(",");
            const toX = xA * cellWidth + 1;
            const toY = yA * cellWidth + 1;

            ctx.beginPath();
            ctx.moveTo(fromX, fromY);
            ctx.lineTo(toX, toY);
            ctx.stroke();
        });
    });
};

export const drawSolution = ({ solution, start, end, ctx, cellWidth }) => {
    ctx.strokeStyle = "red";
    ctx.lineWidth = 1;
    ctx.lineCap = "square";

    solution.forEach((el, i) => {
        if (i < solution.length - 1) {
            const [xA, yA] = el.split(",");
            const fromX = xA * cellWidth + 1;
            const fromY = yA * cellWidth + 1;

            const [xB, yB] = solution[i + 1].split(",");
            const toX = xB * cellWidth + 1;
            const toY = yB * cellWidth + 1;

            ctx.beginPath();
            ctx.moveTo(fromX, fromY);
            ctx.lineTo(toX, toY);
            ctx.stroke();
        }
    });

    const [startX, startY] = start.split(",");
    ctx.fillStyle = "blue";
    ctx.fillRect(startX * cellWidth, startY * cellWidth, 2, 2);

    const [endX, endY] = end.split(",");
    ctx.fillStyle = "green";
    ctx.fillRect(endX * cellWidth, endY * cellWidth, 2, 2);
};
function smile(rating) {
  const circles = [
    {cx: 150, cy: 150, rx: 150, ry:150, fill: 'yellow'},
    {cx: 88, cy: 80, rx: 18,  ry: 26, fill: 'black'},
    {cx: 212, cy: 80, rx: 18,  ry: 26, fill: 'black'}
  ];

  const height = 210 - 100*(rating - 0.5);

  let controlPoints = [
    [60,height],
    [150,210],
    [240,height]
  ];

  if (rating < 0.5) {
    controlPoints = [...controlPoints,
                     [150, 228],
                     [60, height]
                   ];
  }
  const svgElement = d3.selectAll('.smile svg')
                       .attrs({
                          width: 300,
                          height: 300
                        });

  const lineGenerator = d3.line()
                          .curve(d3.curveCardinal);
  const pathData = lineGenerator(controlPoints);

  svgElement.selectAll('ellipse')
            .data(circles)
            .enter()
            .append('ellipse')
            .attrs( d => {
              return {
                cx: d.cx,
                cy: d.cy,
                rx: d.rx,
                ry: d.ry
              }
            })
            .style('fill', (d) => d.fill);

  svgElement.selectAll('path').remove();

  svgElement.append('path')
            .attr('d', pathData)
            .attr('stroke-width', 6)
            .attr('stroke', 'black');
}

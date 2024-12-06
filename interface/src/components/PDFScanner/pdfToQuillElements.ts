import { useState } from 'react';
import * as pdfjsLib from 'pdfjs-dist';
import 'pdfjs-dist/build/pdf.worker.entry';

pdfjsLib.GlobalWorkerOptions.workerSrc = '//cdnjs.cloudflare.com/ajax/libs/pdf.js/2.6.347/pdf.worker.min.js';

export const usePdfToText = () => {
  const [pdfText, setPdfText] = useState('');

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files![0];
    if (file) {
      const typedarray = await file.arrayBuffer();
      const pdf = await pdfjsLib.getDocument(typedarray).promise;
      let text = '';

      for (let i = 1; i <= pdf.numPages; i++) {
        const page = await pdf.getPage(i);
        const content = await page.getTextContent();

        // Lista para almacenar las líneas de texto con sus posiciones
        const lines: { y: number; items: { x: number; str: string }[] }[] = [];

        // Recolectar todos los items con sus posiciones
        content.items.forEach((item: any) => {
          const x = item.transform[4];
          const y = item.transform[5];
          const str = item.str;

          // Buscar la línea correspondiente basándose en 'y'
          let line = lines.find((l) => Math.abs(l.y - y) < 1);
          if (!line) {
            line = { y, items: [] };
            lines.push(line);
          }

          line.items.push({ x, str });
        });

        // Ordenar las líneas por posición Y (vertical) de arriba a abajo
        lines.sort((a, b) => b.y - a.y);

        // Determinar el mínimo x para las indentaciones
        const allX = content.items.map((item: any) => item.transform[4]);
        const minX = Math.min(...allX);

        let previousY: number | null = null; // Variable para almacenar la posición Y de la línea anterior

        // Procesar cada línea
        lines.forEach((line) => {
          // Ordenar los items de la línea por posición X (horizontal) de izquierda a derecha
          line.items.sort((a, b) => a.x - b.x);

          // Detectar posibles columnas basándonos en la diferencia de 'x' entre items
          const columns: { x: number; str: string }[][] = [];
          let currentColumn: { x: number; str: string }[] = [];
          let lastX = -Infinity;
          line.items.forEach((item) => {
            if (item.x - lastX > 50) {
              // Nueva columna (ajusta el umbral según sea necesario)
              if (currentColumn.length > 0) columns.push(currentColumn);
              currentColumn = [];
            }
            currentColumn.push(item);
            lastX = item.x;
          });
          if (currentColumn.length > 0) columns.push(currentColumn);

          // Construir el texto de la línea con separadores de columna, omitiendo columnas vacías
          const lineText = columns
            .map((col) => col.map((item) => item.str).join(' ').trim())
            .filter((colText) => colText.length > 0);

          // Calcular la indentación basada en la posición x mínima de la línea
          const indentLevel = Math.round((line.items[0].x - minX) / 10);
          const indentation = '&nbsp;'.repeat(indentLevel);

          // Añadir un salto de línea adicional si la diferencia en 'y' es significativa
          if (previousY !== null && previousY - line.y > 20) { // Ajusta el umbral según sea necesario
            text += '<br/>';
          }

          // Añadir la línea al texto con la indentación
          text += `${indentation}${lineText.join(' | ')}<br/>`;

          // Actualizar previousY
          previousY = line.y;
        });
      }

      setPdfText(text);
      return text;
    }
  };

  return { pdfText, handleFileUpload, setPdfText };
};

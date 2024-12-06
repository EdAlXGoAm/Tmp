import { useState, useEffect } from 'react';
  
const divWidthElement = () => {

  const [divWidth, setDivWidth] = useState('75%');

  useEffect(() => {
    const updateWidth = () => {
      const newWidth = window.innerWidth * 0.3;
      setDivWidth(`${newWidth}px`);
    };

    window.addEventListener('resize', updateWidth);
    updateWidth(); // Inicializa el ancho al cargar el componente

    return () => window.removeEventListener('resize', updateWidth);
  }, []);

  return divWidth;
}

export default divWidthElement;

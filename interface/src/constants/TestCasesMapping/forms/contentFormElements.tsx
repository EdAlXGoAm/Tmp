import React, { useState } from 'react';

interface ContentFormElementsProps {
  onCleanData: () => void;
  elementToEdit: { key: string, value: any } | null;
  updateContent: (key: string, value: any) => void;
  createContent: (value: string) => void;
  setIsOpenExternal: React.Dispatch<React.SetStateAction<boolean>>;
}

export const ContentFormElements = ({ onCleanData, elementToEdit, updateContent, createContent, setIsOpenExternal }: ContentFormElementsProps) => {
  
  const emptyElementData = {
    key: '',
    value: []
  }
  
  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const [formData, setFormData] = useState(emptyElementData);

  const handleClose = () => {
    setError(null);
    setIsOpen(false);
    setFormData(emptyElementData);
    onCleanData();
    setIsOpenExternal(false);
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { value } = e.target;
    setFormData((prevData: any) => ({ ...prevData, 
      value: prevData.value.map((validation: string, index: number) => 
        index === parseInt(e.target.name.split('[')[1].split(']')[0]) ? JSON.parse(value) : validation
      )
    }));
  }

  const handleSubmit = (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      if(elementToEdit) {
        updateContent(elementToEdit.key, formData.value);
      } else {
        createContent(formData.value.join(', '));
      }
      handleClose();
    } catch (error) {
      setError("Error al crear el contenido");
    } finally {
      setLoading(false);
    }
  }

  return {
    isOpen, setIsOpen,
    error, setError,
    loading, setLoading,
    formData, setFormData,
    handleClose, handleChange, handleSubmit
  }
}

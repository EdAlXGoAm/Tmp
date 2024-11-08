import React, { useState, useEffect } from 'react';

interface TypeElementsProps {
  onCleanData?: () => void,
  elementToEdit?: { key: string, value: string },
  updateType: (key: string, value: string) => void,
  createType: (value: string) => void,
}

export const TypeFormElements = ({ onCleanData, elementToEdit, updateType, createType }: TypeElementsProps) => {

  const emptyElementData = ""

  const [isOpen, setIsOpen] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(false);

  const [formData, setFormData] = useState(emptyElementData);

  const handleClose = () => {
    setError(null);
    setIsOpen(false);
    setFormData(emptyElementData);
    if(onCleanData) onCleanData();
  }

  const handleChange = (
    e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>
  ) => {
    const { value } = e.target;
    setFormData(value);
  }

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    console.log('handleSubmit')
    e.preventDefault();
    setLoading(true);
    try {
      if(elementToEdit) {
        updateType(elementToEdit.key, formData);
      } else {
        createType(formData);
      }
      handleClose();
    } catch (error) {
      setError("Error al crear el tipo");
    } finally {
      setLoading(false);
    }
  }

  return {
    emptyElementData,
    isOpen, setIsOpen,
    error, setError,
    loading, setLoading,
    formData, setFormData,
    handleChange,
    handleSubmit,
    handleClose
  }
}

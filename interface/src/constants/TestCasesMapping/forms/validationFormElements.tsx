import React, { useState } from 'react';

interface ValidationFormElementsProps {
  onCleanData: () => void;
  elementToEdit: { key: string, value: any } | null;
  updateValidation: (key: string, value: any) => void;
  createValidation: (value: string) => void;
}

export const ValidationFormElements = ({ onCleanData, elementToEdit, updateValidation, createValidation }: ValidationFormElementsProps) => {

  const emptyElementData = {
    type: false, // false: string, true: array
    value: ''
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
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { value } = e.target;
    if (e.target.name === 'value') {
      setFormData((prevData: any) => ({ ...prevData, [e.target.name]: value }));
    }
    else { // value[index]
      setFormData((prevData: any) => ({ ...prevData, 
        value: prevData.value.map((validation: string, index: number) => 
          index === parseInt(e.target.name.split('[')[1].split(']')[0]) ? value : validation
        )
      }));
    }
  }

  const handleChangeCheckbox = (
    e: React.ChangeEvent<HTMLInputElement>
  ) => {
    setFormData((prevData: any) => ({ ...prevData, [e.target.name]: e.target.checked }));
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setLoading(true);
    try {
      if(elementToEdit) {
        updateValidation(elementToEdit.key, formData.value);
      } else {
        createValidation(formData.value);
      }
      handleClose();
    } catch (error) {
      setError("Error al crear la validación");
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
    handleChangeCheckbox,
    handleSubmit,
    handleClose
  }
}


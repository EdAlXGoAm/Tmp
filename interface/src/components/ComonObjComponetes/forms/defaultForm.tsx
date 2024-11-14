import React, { useEffect } from 'react';
import styles from '../../../styles/forms/defaultForm.module.css';
import { DefaultFormElements } from '../../../constants/TestCasesMapping/forms/defaultFormElements';
import { RowForm } from '../../../utils/formatUtils';

interface DefaultFormProps {
  elementToEdit: { key: string, value: any, type: boolean, validation: string[] | string } | null;
  onCleanData: () => void;
  isOpenExternal: boolean;
  setIsOpenExternal: React.Dispatch<React.SetStateAction<boolean>>;
  updateDefault: (key: string, value: any) => void;
  createDefault: (value: string) => void;
}

const DefaultForm: React.FC<DefaultFormProps> = ({
  elementToEdit,
  onCleanData,
  isOpenExternal,
  updateDefault,
  createDefault
}) => {
  const {
    isOpen, setIsOpen,
    error,
    loading,
    formData, setFormData,
    handleChange,
    handleSubmit,
    handleClose
  } = DefaultFormElements({ onCleanData, elementToEdit, updateDefault, createDefault });

  useEffect(() => {
    if (elementToEdit) {
      if (elementToEdit.type) {
        if (Array.isArray(elementToEdit.value)) {
          setFormData((prevData: any) => ({ ...prevData, type: true, value: elementToEdit.value }));
        } else {
          const value = elementToEdit.value.split(',');
          setFormData((prevData: any) => ({ ...prevData, type: true, value: value }));
        }
      } else {
        if (Array.isArray(elementToEdit.value)) {
          const value = elementToEdit.value.join(',');
          setFormData((prevData: any) => ({ ...prevData, type: false, value: value }));
        } else {
          setFormData((prevData: any) => ({ ...prevData, type: false, value: elementToEdit.value }));
        }
      }
      setIsOpen(true);
    }
  }, [elementToEdit]);

  useEffect(() => {
    setIsOpen(isOpenExternal);
  }, [isOpenExternal]);

  return (
    <>
      {isOpen && (
        <div className={styles.overlay} onClick={handleClose}>
          <div className={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h2>{elementToEdit ? 'Edit Default' : 'Add Default'}</h2>
            <form onSubmit={handleSubmit}>
              <RowForm>
                <label>Default</label>
                {formData.type ? (
                  typeof formData.value === 'object' && Array.isArray(formData.value) && 
                  <>
                    <div className={styles.statesListBox}>
                      <button className={`${styles.statesListBoxButton} ${styles.statesListBoxAddButton}`}
                        type="button"
                        onClick={() => setFormData({ ...formData, value: [...formData.value, ''] })}
                      >
                        Agregar Default
                      </button>
                      {formData.value.map((value: string, index: number) => (
                        elementToEdit && Array.isArray(elementToEdit?.validation) && elementToEdit.validation.length > 0 ? (
                          <div key={index}>
                            <RowForm>
                              <select className={styles.nomodalInput} name={`value[${index}]`} value={value} onChange={handleChange}>
                                <option value="">Selecciona un valor</option>
                                {elementToEdit.validation.map((validation: string, index: number) => (
                                  <option key={index} value={validation}>{validation}</option>
                                ))}
                              </select>
                              <button className={`${styles.statesListBoxButton} ${styles.statesListBoxDeleteButton}`}
                                type="button"
                                onClick={() => setFormData({ ...formData, value: formData.value.filter((_, i) => i !== index) })}
                              >
                                Eliminar
                              </button>
                            </RowForm>
                          </div>
                        ) : (
                          <div key={index}>
                            <RowForm>
                              <input className={styles.nomodalInput} type="text" name={`value[${index}]`} value={value} onChange={handleChange} />
                              <button className={`${styles.statesListBoxButton} ${styles.statesListBoxDeleteButton}`}
                                type="button"
                                onClick={() => setFormData({ ...formData, value: formData.value.filter((_, i) => i !== index) })}
                              >
                                Eliminar
                              </button>
                            </RowForm>
                          </div>
                        )
                      ))}
                    </div>
                  </>
                ) : (
                  <input type="text" name="value" value={formData.value} onChange={handleChange} />
                )}
              </RowForm>
              {error && <p className={styles.error}>{error}</p>}
              <div className={styles.buttons}>
                <button type="submit" disabled={loading}>
                  {loading ? 'Updating...' : (elementToEdit ? 'Update' : 'Add')}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}

export default DefaultForm;

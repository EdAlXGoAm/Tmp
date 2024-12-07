import React, { useEffect, useState } from 'react';
import { open, save } from '@tauri-apps/plugin-dialog';
import 'react-quill/dist/quill.snow.css';
import styles from './pdfToQuill.module.css';
import { Column, ColumnTextCentered, MiddleColumn, Row, RowForm, Subtitle, Titles } from '../../utils/formatUtils';
import { Tabs, Tab } from '@mui/material';
import { TabPanel } from './TabPanel';
import divWidthElement from './DimensionElements';
import { invoke } from "@tauri-apps/api/core";

const PdfToQuill: React.FC = () => {

  const [path_of_file, setPathOfFile] = useState('');
  const [page_indicada_from, setPageIndicadaFrom] = useState(6);
  const [page_indicada_to, setPageIndicadaTo] = useState(6);
  const handleFileChange = async () => {
    const selectedFile = await open({
        filters: [{ name: 'PDF Files', extensions: ['pdf'] }],
        defaultPath: 'D:/DemoFiles'
      });
    setPathOfFile(selectedFile || '');
  };

  const [_textoFromPython, setTextoFromPython] = useState('');
  const [textoFromPython_HTML, setTextoFromPythonHTML] = useState('');

  const getText = async () => {
    function formatTextForHtml(text: string): string {
      return text
        .split('\n')
        .map((line: string) => line.replace(/^\s+/gm, (match: string) => '&nbsp;'.repeat(match.length)))
        .join('<br/>');
    }
    const response_text = await fetch('http://127.0.0.1:5000/api/pdf_to_text_tables_text', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        pdf_path: path_of_file,
        output_dir: `${path_of_file.split('\\').slice(0, -1).join('/')}/tmp`,
        page_indicada_from: page_indicada_from,
        page_indicada_to: page_indicada_to
      })
    });
    const data_text = await response_text.json();
    setTextoFromPython(formatTextForHtml(data_text.text));

    const response_html = await fetch('http://127.0.0.1:5000/api/pdf_to_text_tables_html', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        pdf_path: path_of_file,
        output_dir: `${path_of_file.split('\\').slice(0, -1).join('/')}/tmp`,
        page_indicada_from: page_indicada_from,
        page_indicada_to: page_indicada_to
      })
    });
    const data_html = await response_html.json();
    setTextoFromPythonHTML(formatTextForHtml(data_html.text));
  }
  

  const a11yProps = (index: number) => {
    return {
      id: `tab-${index}`,
      'aria-controls': `tabpanel-${index}`,
    };
  }
  const [valueTabs, setValueTabs] = useState(0);
  const [valueTabsDescarted, setValueTabsDescarted] = useState(0);
  const handleChangeTabs = (_event: React.SyntheticEvent, newValue: number) => {
    console.log(newValue);
    setValueTabs(newValue);
  };
  const handleChangeTabsDescarted = (_event: React.SyntheticEvent, newValue: number) => {
    console.log(newValue);
    setValueTabsDescarted(newValue);
  };

  const [path_of_mapping, setPathOfMapping] = useState('');
  const [index_to_search, setIndexToSearch] = useState('');
  const handleMappingFileChange = async () => {
    const selectedFile = await open({
        filters: [{ name: 'Mapping Files', extensions: ['json'] }],
        defaultPath: 'D:/edalxgoam/Tmp/MAPP'
      });
    setPathOfMapping(selectedFile || '');
  };
  interface Paragraphs {
    paragraphs: any[];
    paragraphs_descarted: any[];
    element: any;
  }
  const [paragraphs, setParagraphs] = useState<Paragraphs>({
    paragraphs: [],
    paragraphs_descarted: [],
    element: {}
  });
  const [displayParagraphs, setDisplayParagraphs] = useState([]);
  const [displayDescartedParagraphs, setDisplayDescartedParagraphs] = useState([]);
  const getIndexes = async () => {
    const response_text = await fetch('http://127.0.0.1:5000/api/get_index_tree', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        pdf_path: path_of_file,
        output_dir: `${path_of_file.split('\\').slice(0, -1).join('/')}/tmp`,
        mapping_path: path_of_mapping,
        index_to_search: index_to_search
      })
    });
    let data_text = await response_text.json();
    const display_data_text = data_text.paragraphs.map((paragraph: any) => {
      const processedParagraph = paragraph.paragraph
        .split('\n')
        .map((line: string) => {
          if (line.startsWith('## ')) {
            return `<span style="color: red;">${line.slice(3)}</span>`;
          }
          return line;
        })
        .join('\n');

      const replacedParagraph = processedParagraph
        .split('\n')
        .map((line: string) => line.replace(/^\s+/gm, (match: string) => '&nbsp;'.repeat(match.length)))
        .join('<br/>');
      
      return {
        ...paragraph,
        paragraph: replacedParagraph
      };
    });
    data_text.paragraphs = data_text.paragraphs.map((paragraph: any) => {
      console.log(paragraph);
      const sectionsToReplace = ['Preparation', 'Main Part', 'Completion'];
      sectionsToReplace.forEach((sectionKey) => {
        if (paragraph.element[sectionKey]) {
          const replacedSection = paragraph.element[sectionKey]
            .split('\n')
            .map((line: string) => line.replace(/^\s+/gm, (match: string) => '&nbsp;'.repeat(match.length)))
            .join('<br>');
          
          paragraph.element[sectionKey] = replacedSection;
        }
      });
      return paragraph;
    });
    setParagraphs(data_text);
    setDisplayParagraphs(display_data_text);
    console.log(data_text);
    const display_data_descarted = data_text.paragraphs_descarted.map((paragraph: any) => {
      const processedParagraph = paragraph.paragraph
        .split('\n')
        .map((line: string) => {
          if (line.startsWith('## ')) {
            return `<span style="color: red;">${line.slice(3)}</span>`;
          }
          return line;
        })
        .join('\n');

      const replacedParagraph = processedParagraph
        .split('\n')
        .map((line: string) => line.replace(/^\s+/gm, (match: string) => '&nbsp;'.repeat(match.length)))
        .join('<br/>');
      
      return {
        ...paragraph,
        paragraph: replacedParagraph
      };
    });
    setDisplayDescartedParagraphs(display_data_descarted);
  }

  const divWidth = divWidthElement();

  const backgroundDecider = (paragraph: any) => {
    if (paragraph.title.startsWith('3')) {
      return 'lightblue';
    }
    if (paragraph.mainpart_added) {
      return paragraph.mainpart_added;
    }
    return 'inherit';
  }

  // Nuevo estado para controlar si el contenido está colapsado
  const [isCollapsed, setIsCollapsed] = useState(false);

  // Efecto para colapsar cuando textoFromPython_HTML tiene contenido
  useEffect(() => {
    if (textoFromPython_HTML) {
      setIsCollapsed(true);
    } else {
      setIsCollapsed(false);
    }
  }, [textoFromPython_HTML]);

  // Función para manejar el clic en la burbuja
  const handleBubbleClick = () => {
    setIsCollapsed(!isCollapsed);
    // Si deseas limpiar el contenido al expandir nuevamente
    // setTextoFromPythonHTML('');
  };

  const [valueTabsResusableFunctions, setValueTabsResusableFunctions] = useState(0);

  const handleChangeTabsResusableFunctions = (_event: React.SyntheticEvent, newValue: number) => {
    console.log(newValue);
    setValueTabsResusableFunctions(newValue);
  };
  
  const [index_to_search_ResusableFunctions, setIndexToSearchResusableFunctions] = useState('');
  const [paragraphs_ResusableFunctions, setParagraphsResusableFunctions] = useState([] as any);
  const [displayResusableFunctions, setDisplayResusableFunctions] = useState([]);

  const getIndexesResusableFunctions = async () => {
    const response_text = await fetch('http://127.0.0.1:5000/api/get_index_tree', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        pdf_path: path_of_file,
        output_dir: `${path_of_file.split('\\').slice(0, -1).join('/')}/tmp`,
        mapping_path: path_of_mapping,
        index_to_search: index_to_search_ResusableFunctions
      })
    });
    let data_text = await response_text.json();
    setParagraphsResusableFunctions(data_text);
    const display_data_text = data_text.paragraphs.map((paragraph: any) => {
      const processedParagraph = paragraph.paragraph
        .split('\n')
        .map((line: string) => {
          if (line.startsWith('## ')) {
            return `<span style="color: red;">${line.slice(3)}</span>`;
          }
          return line;
        })
        .join('\n');

      const replacedParagraph = processedParagraph
        .split('\n')
        .map((line: string) => line.replace(/^\s+/gm, (match: string) => '&nbsp;'.repeat(match.length)))
        .join('<br/>');
      
      return {
        ...paragraph,
        paragraph: replacedParagraph
      };
    });
    setDisplayResusableFunctions(display_data_text);
  }

  const addFunctionsToElement = async () => {
    const response_text = await fetch('http://127.0.0.1:5000/api/replaceFunctions', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        paragraphs: paragraphs.paragraphs,
        paragraphs_reusable: paragraphs_ResusableFunctions.paragraphs
      })
    });
    const data_text = await response_text.json();
    setParagraphs(data_text);
  }
  
  const saveParagraphsToFile = async (paragraphs: any[]) => {
    const selectedPath = await save({
      filters: [{ name: 'JSON Files', extensions: ['json'] }],
      defaultPath: 'D:/edalxgoam/Tmp/MAPP/Paragraphs.json'
    });
    const paragraphsFile = JSON.stringify(paragraphs, null, 2);
    invoke('write_file', { path: selectedPath as string, data: paragraphsFile });
  }
  
  const onSaveParagraphsFile = () => {
    if (paragraphs.paragraphs.length > 0) {
      saveParagraphsToFile(paragraphs.paragraphs);
    }
  };
  return (
    <div className={styles.container}>
      <Row>
        <Column>
          <div className={styles.bubble} onClick={handleBubbleClick}>
            <img
            src="https://img.freepik.com/vector-premium/plantilla-vector-icono-documento-hoja-papel_917138-2010.jpg" 
            alt="Icono de documento" />
          </div>
          {!isCollapsed &&
            // Mostrar formulario cuando no está colapsado
            <div className={styles.floatingDiv}>
              <RowForm>
                <ColumnTextCentered>
                  <h2>PDF Scanner por Python</h2>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <button onClick={handleFileChange}>Seleccionar Archivo</button>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <p style={{ fontSize: '11px' }}>{path_of_file}</p>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <label>Número de página</label>
                  <Row>
                  <Column>
                    <span style={{ fontSize: '12px' }}>Desde </span>
                    <input
                      type="number"
                      value={page_indicada_from}
                      onChange={(event) => setPageIndicadaFrom(parseInt(event.target.value))}
                      style={{ width: '80px' }}
                    />
                    <span style={{ fontSize: '12px' }}> Hasta </span>
                    <input
                      type="number"
                      value={page_indicada_to}  
                      onChange={(event) => setPageIndicadaTo(parseInt(event.target.value))}
                      style={{ width: '80px' }}
                    />
                  </Column>
                  </Row>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <button onClick={getText}>Obtener Texto</button>
                </ColumnTextCentered>
              </RowForm>
              {/* Aquí puedes decidir si mostrar el contenido de textoFromPython_HTML */}
              {/* Puedes continuar mostrando textoFromPython_HTML si lo deseas */}
              {textoFromPython_HTML && (
                <div
                  className={styles.htmlContainer}
                  style={{ marginTop: '20px', fontSize: '11px' }}
                  dangerouslySetInnerHTML={{ __html: textoFromPython_HTML || '' }}
                />
              )}
            </div>
          }
        </Column>
      </Row>
      {textoFromPython_HTML &&
        <>
          <Row>
            <Column width={6}>
              <RowForm>
                <ColumnTextCentered>
                  <h2>Now will get the indexes</h2>
                  <label> Select the Mapping File</label>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <button onClick={handleMappingFileChange}>Select File</button>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <p style={{ fontSize: '11px' }}>{path_of_mapping}</p>
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <label style={{ marginRight: '10px' }}>Index to Search</label>
                  <input style={{ width: '80px' }} type="text" value={index_to_search} onChange={(event) => setIndexToSearch(event.target.value)} />
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <button onClick={getIndexes} style={{
                    fontSize: '11px',
                    backgroundColor: 'green',
                    borderRadius: '10px',
                    border: 'none',
                    padding: '5px'
                  }}>Get Indexes</button>
                </ColumnTextCentered>
              </RowForm>
            </Column>
          </Row>
          <Row>
            <MiddleColumn>
              <div>
                <Subtitle mt={0}>Paragraphs</Subtitle>
                {displayParagraphs && displayParagraphs.length > 0 && (
                  <>
                    <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', marginBottom: '10px' }}>
                      <div style={{ width: '10px', height: '10px', backgroundColor: '#03fc8c', marginRight: '5px' }}></div>
                      <span>
                        <span style={{ color: 'green' }}>Test Case ID:</span>, 
                        <span style={{ color: 'green' }}>Main Part</span>,
                        <span style={{ color: 'green' }}>Description</span>
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', marginBottom: '10px' }}>
                      <div style={{ width: '10px', height: '10px', backgroundColor: '#03fcf8', marginRight: '5px' }}></div>
                      <span>
                        <span style={{ color: 'green' }}>Test Case ID:</span>, 
                        <span style={{ color: 'green' }}>Main Part</span>, 
                        <span style={{ color: 'red' }}>Description</span>
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', marginBottom: '10px' }}>
                      <div style={{ width: '10px', height: '10px', backgroundColor: '#0390fc', marginRight: '5px' }}></div>
                      <span>
                        <span style={{ color: 'green' }}>Test Case ID:</span>, 
                        <span style={{ color: 'red' }}>Main Part</span>, 
                        <span style={{ color: 'red' }}>Description</span>
                      </span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', marginBottom: '10px' }}>
                      <div style={{ width: '10px', height: '10px', backgroundColor: '#eebf3e', marginRight: '5px' }}></div>
                      <span>
                        <span style={{ color: 'red' }}>Test Case ID:</span>, 
                        <span style={{ color: 'red' }}>Main Part</span>, 
                        <span style={{ color: 'red' }}>Description</span>
                      </span>
                      <span style={{ color: 'black', fontStyle: 'italic' }}>&nbsp;→ COULD BE A NET TEST CASE</span>
                    </div>
                    <div style={{ display: 'flex', alignItems: 'center', fontSize: '10px', marginBottom: '10px' }}>
                      <div style={{ width: '10px', height: '10px', backgroundColor: '#e61b1b', marginRight: '5px' }}></div>
                      <span>
                        <span style={{ color: 'red' }}>Test Case ID:</span>, 
                        <span style={{ color: 'red' }}>Main Part</span>, 
                        <span style={{ color: 'red' }}>Description</span>
                      </span>
                      <span style={{ color: 'black', fontStyle: 'italic' }}>&nbsp;→ IS NOT A TEST CASE</span>
                    </div>
                  </>
                )}
                {displayParagraphs && displayParagraphs.length > 0 && (
                  <>
                    <div style={{ display: 'flex', maxHeight: '50vh', overflowY: 'auto' }}>
                      <Tabs
                        orientation="vertical"
                        value={valueTabs}
                        onChange={handleChangeTabs}
                        variant="scrollable"
                        scrollButtons="auto"
                        aria-label="TestCase Tabs"
                        sx={{ borderRight: 1, borderColor: 'divider', fontSize: '11px' }}
                      >
                        {displayParagraphs.map((paragraph: any, i: number) => (
                          <Tab 
                          key={i}
                          label={`${paragraph.title}`}
                          {...a11yProps(i)}
                          style={{
                            fontSize: '11px',
                            backgroundColor: backgroundDecider(paragraph)
                          }}
                          title={paragraph.tooltip}
                          />
                        ))}
                      </Tabs>
                      {displayParagraphs.map((paragraph: any, i: number) => (
                        <TabPanel value={valueTabs} index={i} key={i}>
                          <div className="card-body" style={{
                            border: '1px solid grey',
                            borderRadius: '10px',
                            boxShadow: '0px 0px 20px 5px rgba(0, 0, 0, 0.1)',
                            padding: '20px',
                            width: divWidth
                          }}>
                            <Titles mt={0}>{`${paragraph.title}`}</Titles>
                            <Row mb={0} mt={0}>
                              <Column>
                                <div style={{ fontSize: '11px' }}
                                dangerouslySetInnerHTML={{ __html: paragraph.paragraph }} />
                              </Column>
                            </Row>
                          </div>
                        </TabPanel>
                      ))}
                    </div>
                  </>
                )}
              </div>
              <div>
                <Subtitle mt={0}>Descarted Paragraphs</Subtitle>
                {displayDescartedParagraphs && displayDescartedParagraphs.length > 0 && (
                  <>
                    <div style={{ display: 'flex', maxHeight: '50vh', overflowY: 'auto' }}>
                      <Tabs
                        orientation="vertical"
                        value={valueTabsDescarted}
                        onChange={handleChangeTabsDescarted}
                        variant="scrollable"
                        scrollButtons="auto"
                        aria-label="TestCase Tabs"
                        sx={{ borderRight: 1, borderColor: 'divider', fontSize: '11px' }}
                      >
                        {displayDescartedParagraphs.map((paragraph: any, i: number) => (
                          <Tab 
                          key={i}
                          label={`${paragraph.title}`}
                          {...a11yProps(i)}
                          style={{
                            fontSize: '11px',
                            backgroundColor: backgroundDecider(paragraph)
                          }}
                          title={paragraph.tooltip}
                          />
                        ))}
                      </Tabs>
                      {displayDescartedParagraphs.map((paragraph: any, i: number) => (
                        <TabPanel value={valueTabsDescarted} index={i} key={i}>
                          <div className="card-body" style={{
                            border: '1px solid grey',
                            borderRadius: '10px',
                            boxShadow: '0px 0px 20px 5px rgba(0, 0, 0, 0.1)',
                            padding: '20px',
                            width: divWidth
                          }}>
                            <Titles mt={0}>{`${paragraph.title}`}</Titles>
                            <Row mb={0} mt={0}>
                              <Column>
                                <div style={{ fontSize: '11px' }}
                                dangerouslySetInnerHTML={{ __html: paragraph.paragraph }} />
                              </Column>
                            </Row>
                          </div>
                        </TabPanel>
                      ))}
                    </div>
                  </>
                )}
              </div>
            </MiddleColumn>
            <MiddleColumn>
              <RowForm>
                <ColumnTextCentered>
                  <label style={{ marginRight: '10px' }}>Index to Search</label>
                  <input style={{ width: '80px' }} type="text" value={index_to_search_ResusableFunctions} onChange={(event) => setIndexToSearchResusableFunctions(event.target.value)} />
                </ColumnTextCentered>
              </RowForm>
              <RowForm>
                <ColumnTextCentered>
                  <button onClick={getIndexesResusableFunctions} style={{
                    fontSize: '11px',
                    backgroundColor: 'green',
                    borderRadius: '10px',
                    border: 'none',
                    padding: '5px'
                  }}>Get Indexes</button>
                </ColumnTextCentered>
              </RowForm>
              <Row>
                <MiddleColumn width={9}>
                  {displayResusableFunctions && displayResusableFunctions.length > 0 && (
                    <>
                      <div style={{
                        display: 'flex',
                        flexDirection: 'column',
                        maxHeight: '20vh',
                        overflowY: 'auto',
                        border: '1px solid grey',
                        borderRadius: '10px',
                        boxShadow: '0px 0px 20px 5px rgba(0, 0, 0, 0.1)',
                        padding: '20px',
                      }}>
                        <Tabs
                          orientation="horizontal"
                          value={valueTabsResusableFunctions}
                          onChange={handleChangeTabsResusableFunctions}
                          variant="scrollable"
                          scrollButtons="auto"
                          aria-label="TestCase Tabs"
                          sx={{ borderBottom: 1, borderColor: 'divider', fontSize: '11px' }}
                        >
                          {displayResusableFunctions.map((paragraph: any, i: number) => (
                            <Tab 
                            key={i}
                            label={`${paragraph.title}`}
                            {...a11yProps(i)}
                            style={{
                              fontSize: '11px',
                              backgroundColor: backgroundDecider(paragraph)
                            }}
                            title={paragraph.tooltip}
                            />
                          ))}
                        </Tabs>
                        {displayResusableFunctions.map((paragraph: any, i: number) => (
                          <TabPanel value={valueTabsResusableFunctions} index={i} key={i}>
                            <div className="card-body" style={{
                              border: '1px solid grey',
                              borderRadius: '10px',
                              boxShadow: '0px 0px 20px 5px rgba(0, 0, 0, 0.1)',
                              padding: '20px',
                              width: parseInt(divWidth)*0.8
                            }}>
                              <Titles mt={0}>{`${paragraph.title}`}</Titles>
                              <Row mb={0} mt={0}>
                                <Column>
                                  <div style={{ fontSize: '10px' }}
                                  dangerouslySetInnerHTML={{ __html: paragraph.paragraph }} />
                                </Column>
                              </Row>
                            </div>
                          </TabPanel>
                        ))}
                      </div>
                    </>
                  )}
                </MiddleColumn>
                <MiddleColumn width={3}>
                  <RowForm>
                    <ColumnTextCentered>
                      <button
                      className={styles.buttonAddFunctions}
                      onClick={addFunctionsToElement}>Add Functions</button>
                    </ColumnTextCentered>
                    <ColumnTextCentered>
                      <p style={{ fontSize: '10px' }}>This actions will try to add the functions to the elements with label '(page xx)'</p>
                    </ColumnTextCentered>
                  </RowForm>
                </MiddleColumn>
              </Row>
              <RowForm>
                <ColumnTextCentered>
                  <button onClick={onSaveParagraphsFile}>Save Paragraphs</button>
                </ColumnTextCentered>
              </RowForm>
              <Subtitle mt={0}>Elements</Subtitle>
              <div>
                {paragraphs && paragraphs.paragraphs[valueTabs] && (
                  <div style={{ fontSize: '12px', marginTop: '10px' }}>
                    <label>Title:</label>
                    <p>{paragraphs.paragraphs[valueTabs].title}</p>
                    <label>Description:</label>
                    <p>{paragraphs.paragraphs[valueTabs].description}</p>
                    {paragraphs.paragraphs[valueTabs].element && Object.keys(paragraphs.paragraphs[valueTabs].element).map((key: string, _i: number) => (
                      <>
                        <label style={{ fontStyle: 'italic', fontWeight: 'bold' }}>{key}</label>
                        <div>{
                          paragraphs.paragraphs[valueTabs].element[key].includes('<table') ||
                          paragraphs.paragraphs[valueTabs].element[key].includes('<br')
                          ? <div
                            style={{
                              marginBottom: '10px'
                            }}
                            dangerouslySetInnerHTML={{ __html: paragraphs.paragraphs[valueTabs].element[key] }} />
                          : <p>{paragraphs.paragraphs[valueTabs].element[key]}</p>
                        }</div>
                      </>
                    ))}
                  </div>
                )}
              </div>
            </MiddleColumn>
          </Row>
        </>
      }
    </div>
  );
};

export default PdfToQuill;

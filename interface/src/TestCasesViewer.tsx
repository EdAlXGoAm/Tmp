import { useState, useEffect } from "react";
import { open } from '@tauri-apps/plugin-dialog';
import { CenteredColumn, Titles, Subtitle, CustomForm } from "./utils/formatUtils";
import MapFillView from "./components/MappingFilledReview/mapFillView";
import "./App.css";

export default function TestCasesViewer() {
  const [file, setFile] = useState<String | null>(null);
  const [width, setWidth] = useState(window.innerWidth < 1200 ? 12 : 6);

  useEffect(() => {
    const handleResize = () => {
      const windowWidth = window.innerWidth;
      setWidth(windowWidth < 1200 ? 12 : 6);
    };
    window.addEventListener('resize', handleResize);
    return () => {
      window.removeEventListener('resize', handleResize);
    };
  }, []);

  const handleFileChange = async () => {
    const selectedFile = await open({
      filters: [{ name: 'JSON Files', extensions: ['json'] }],
      defaultPath: 'D:/edalxgoam/Tmp/MAPP'
    });
    setFile(selectedFile);
  };

  const splitAndFormatString = (file: string) => {
    const fileString = file.split('\\');
    if (fileString.length > 3) {
      return `${fileString[0]}\\${fileString[1]}\\...\\${fileString[fileString.length - 1]}`;
    }
    return file;
  };

  return (
    <div className="container-fluid">
      <Titles>
        <h1>Test Cases Viewer</h1>
      </Titles>
      <Subtitle>Drag and Drop or Select the Mapping JSON file</Subtitle>
      <CenteredColumn mt={0}>
        <div className="FileContainer">
          <button onClick={handleFileChange}>Select JSON File</button>

          {file && 
            <CustomForm>
              <label className="labelFormCustom">Selected file: </label>
              <input className="inputFormCustom" type="text" readOnly
                value={splitAndFormatString(file as string)}
              />
            </CustomForm>
          }
        </div>
      </CenteredColumn>
      <CenteredColumn mt={3} width={width}>
        <MapFillView file={file} />
      </CenteredColumn>
    </div>
  );
}

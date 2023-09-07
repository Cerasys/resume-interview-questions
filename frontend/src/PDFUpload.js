import React from "react";
import { useState } from "react";
import axios from "axios";
import {
  Box,
  CircularProgress,
  CircularProgressLabel,
  Flex,
  Input,
  VStack,
  Text,
  Code,
  Stack,
} from "@chakra-ui/react";

const PDFUpload = () => {
  const [, setfileURL] = useState("");
  const [selectedFile, setselectedFile] = useState(null);
  const [uploadedFile, setuploadedFile] = useState({});
  const [isUploading, setisUploading] = useState(false);
  const [isFileUploaded, setisFileUploaded] = useState(false);
  const [uploadProgress, setuploadProgress] = useState(0);
  const [questions, setQuestions] = useState(null);

  let uploadInput = React.createRef();

  // Track selected file before the upload
  const handleSelectFile = (e) => {
    const selectedFileList = [];
    for (let i = 0; i < e.target.files.length; i++) {
      selectedFileList.push(e.target.files.item(i));
    }
    setselectedFile(selectedFileList);
  };

  // Upload file to server
  const handleUploadFile = async (ev) => {
    ev.preventDefault();

    setisUploading(true);
    const data = new FormData();
    // Append the file to the request body
    for (let i = 0; i < uploadInput.files.length; i++) {
      data.append("file", uploadInput.files[i], uploadInput.files[i].name);
    }

    try {
      const config = {
        onUploadProgress: (progressEvent) => {
          const { loaded, total } = progressEvent;
          setuploadProgress(Math.round((loaded / total) * 100));
        },
      };
      const response = await axios.post(
        "http://localhost:5000/upload",
        data,
        config
      );
      const body = response.data;
      console.log(body);
      setfileURL(`http://localhost:5000/${body.filename}`);
      if (response.status === 200) {
        setisFileUploaded(true); // flag to show the uploaded file
        setisUploading(false);
        setuploadedFile(selectedFile); // set the uploaded file to show the name
      }
    } catch (error) {
      console.error(error);
      setisUploading(false);
    }
  };

  return (
    <Flex
      align="center"
      direction="column"
      px={20}
      bg={"#444444"}
      minH={"100vh"}
    >
      <Stack
        spacing={4}
        align="center"
        bg={"#F2F2F2"}
        p={20}
        my={20}
        borderRadius={20}
        minH={"90vh"}
      >
        <Box w={500} textAlign="center" px={10}>
          <h1>LPQ PDF Processor</h1>
          <h3>
            By: <a href="mailto:timleungtech@gmail.com">Tim Leung</a>
          </h3>
          <Text fontWeight="bold" color="gray.700">
            This is a file processing web app created with React, Python, and
            Flask to upload PDF files. It parses text in the PDF, retrieves
            necessary strings of each page, and sorts the splitted pages based
            on the strings. Strings are matched with dictionaries to paint
            output strings on canvases. Output file is then saved locally to the
            server and user is prompted to download.
          </Text>
        </Box>
        {/* Upload file form */}
        <form onSubmit={handleUploadFile}>
          <Flex justify="center" align="center" direction="column">
            <label
              htmlFor="file"
              style={{
                cursor: "pointer",
                padding: 10,
                marginBottom: 20,
                border: "1px solid #000",
                borderRadius: 10,
                background: "#698DAF",
                color: "white",
              }}
            >
              Select file to upload
              <Input
                id="file"
                type="file"
                multiple
                ref={(ref) => {
                  uploadInput = ref;
                }}
                onChange={handleSelectFile}
                style={{ display: "none" }}
              />
            </label>
            <VStack bg="azure" p={30} borderRadius={20}>
              <Text fontWeight="bold">Selected file</Text>
              <Flex pb={20} direction="column">
                {selectedFile &&
                  selectedFile.map((item, index) => {
                    return (
                      <Text key={index}>
                        {/* <b>{index + 1}. </b> */}
                        {item.name}
                      </Text>
                    );
                  })}
              </Flex>
              <Box
                as="button"
                type="submit"
                disabled={selectedFile ? false : true}
                p={15}
                textAlign="center"
                fontWeight={600}
                border="1px solid #000"
                borderRadius={10}
                bg={"#698DAF"}
                color={"white"}
                cursor="pointer"
              >
                Upload
              </Box>
            </VStack>
          </Flex>
        </form>
        {/* Show the upload progress */}
        {isUploading && (
          <>
            <CircularProgress value={uploadProgress} thickness="12px">
              <CircularProgressLabel>{uploadProgress}%</CircularProgressLabel>
            </CircularProgress>
          </>
        )}
        {/* Show the success message and file names after upload */}
        {isFileUploaded && (
          <>
            <Flex justify="center" align="center" direction="column">
              <Box p={10} textAlign="center" color={"green"}>
                <h3>File uploaded successfully</h3>
              </Box>
            </Flex>
            <VStack bg="azure" p={30} borderRadius={20}>
              <Text fontWeight="bold">Uploaded file</Text>
              <Flex pb={20} direction="column">
                {uploadedFile &&
                  uploadedFile.map((item, index) => {
                    return (
                      <Text key={index}>
                        {/* <b>{index + 1}. </b> */}
                        {item.name}
                      </Text>
                    );
                  })}
              </Flex>
            </VStack>
          </>
        )}
      </Stack>
    </Flex>
  );
};
export default PDFUpload;

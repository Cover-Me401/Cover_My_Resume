Dropzone.autoDiscover = false;

const myDropzone = new Dropzone("#myDropzone", {
  url: "upload_pdf",
  maxFiles: 1,
  maxFilesize: 1,
  acceptedFiles: '.pdf',
})


// Function to remove an uploaded file
function removeUploadedFile(index) {
    const filesArray = Array.from(dataFileDnD.files);
    filesArray.splice(index, 1);
    dataFileDnD.files = createFileList(filesArray);
}

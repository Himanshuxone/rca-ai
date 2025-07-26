export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);
  try {
    const response = await fetch("http://localhost:8000/api/upload", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Upload failed");
    }

    const data = await response.json();
    console.log("+++++++++++", data)
    return data;
  } catch (error) {
    console.error("Error uploading file:", error);
    return { error: error.message };
  }
}

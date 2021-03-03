import { flaskBackendService } from "../environment";

class ApiService {
  generateDatasetPrediction(csvFile) {
    const formData = new FormData();
    formData.append("file", csvFile);
    return flaskBackendService.request({
      headers: { "Content-Type": "multipart/form-data" },
      method: "post",
      url: "/predict",
      body: formData
    });
  }

  generateDatasetPredictionMock(csvFile) {
    console.log(
      "Recieved Dataset csv file in mock api call: ",
      csvFile.split("\n").slice(0, 6)
    );
    return new Promise(resolve => {
      const predictions = [
        { id: 1, established: "AML", predicted: "AML" },
        { id: 2, established: "CML", predicted: "CML" },
        { id: 3, established: "MDS", predicted: "MDS" },
        { id: 4, established: "MDS", predicted: "MDS" },
        { id: 5, established: "AML", predicted: "AML" },
        { id: 6, established: "AML", predicted: "AML" },
        { id: 7, established: "NHL", predicted: "NHL" },
        { id: 8, established: "APML", predicted: "APML" },
        { id: 9, established: "AML", predicted: "AML" },
        { id: 10, established: "MDS", predicted: "MDS" },
        { id: 11, established: "MPN", predicted: "MPN" },
        { id: 12, established: "CML", predicted: "CML" },
        { id: 13, established: "HL", predicted: "HL" },
        { id: 14, established: "NHL", predicted: "NHL" },
        { id: 15, established: "Control", predicted: "Control" },
        { id: 16, established: "APML", predicted: "APML" },
        { id: 17, established: "AML", predicted: "CML" },
        { id: 18, established: "CML", predicted: "AML" },
        { id: 19, established: "MDS", predicted: "AML" },
        { id: 20, established: "MDS/MPN", predicted: "AML" }
      ];
      setTimeout(() => resolve(predictions), 3000);
    });
  }
}

export default new ApiService();

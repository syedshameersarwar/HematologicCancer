<template>
  <div>
    <div style="text-align: center; margin: 5px; padding: 10px">
      <img id="ned" alt="Ned logo" src="../assets/logo.png" />
      <img id="nipd" alt="Nipd logo" src="../assets/nipd.jpeg" />
      <br />
      <h2>
        Early Screening and Detection of Hematologic Cancer using Complete Blood
        Count
      </h2>
    </div>
    <div class="panel panel-sm">
      <div class="panel-body">
        <div class="form-group">
          <label for="csv_file" class="control-label col-sm-3 text-right"
            >Dataset File to import:
          </label>
          <div class="col-sm-9">
            <input
              style="padding: 3px; margin: 3px"
              type="file"
              id="csv_file"
              name="csv_file"
              class="form-control"
              @change="fetchCsv($event)"
            />
          </div>
        </div>

        <div class="col-sm-offset-3 col-sm-9">
          <button
            :disabled="!csv"
            type="button"
            class="btn btn-primary"
            @click="parseCsv"
          >
            Load Dataset
          </button>

          <button
            :disabled="!csv || !loaded"
            style="margin-left: 40px;"
            type="button"
            class="btn btn-success"
            @click="generatePredictions"
          >
            Generate Prediction's
          </button>

          <a-spin v-if="predictionLoading">
            <a-icon
              slot="indicator"
              type="loading"
              style="font-size: 24px; margin-left: 20px"
              spin
            />
          </a-spin>
        </div>
      </div>
    </div>
    <div style="margin: 30px; padding: 10px">
      <a-collapse v-model="activeKey">
        <template #expandIcon="props">
          <a-icon type="caret-right" :rotate="props.isActive ? 90 : 0" />
        </template>

        <a-collapse-panel
          key="1"
          header="Dataset"
          :disabled="!loaded"
          :style="collapseStyle"
        >
          <a-table
            v-if="data.length > 0"
            :columns="columns"
            :data-source="data"
            :pagination="{ pageSize: 10 }"
            :scroll="{ y: 240, x: 1300 }"
          />
        </a-collapse-panel>
        <a-collapse-panel
          key="2"
          header="Visualization's"
          :disabled="!loaded"
          :style="collapseStyle"
        >
          <div class="row mt-5 mb-4">
            <BarChart
              v-if="data.length > 0"
              :data="data"
              :dimension="{ x: 'Study_Groups' }"
            />
            <BoxChart
              v-if="data.length > 0"
              :data="data"
              :dimension="['Hb', 'WBC', 'PLT', 'per_IG', 'NRBC_per']"
            />
          </div>

          <div class="row mt-5 mb-4">
            <AreaChart
              v-if="data.length > 0"
              :data="data"
              :dimension="{ x: 'Hb', y: 'RBC' }"
            />

            <ScatterChart
              v-if="data.length > 0"
              :data="data"
              :dimension="{ x: 'Hb', y: 'RBC', groupCount: 3 }"
            />
          </div>
        </a-collapse-panel>
        <a-collapse-panel
          key="3"
          header="Prediction's Panel"
          :disabled="!predictionsLoaded"
          :style="collapseStyle"
        >
          <a-table
            v-if="predictions"
            :columns="predictionColumns"
            :data-source="predictions"
            :pagination="{ pageSize: 10 }"
            :scroll="{ y: 240, x: 1300 }"
          />

          <div class="row mt-5 mb-4">
            <MultiBarChart
              v-if="Object.keys(report).length > 0"
              :data="report"
            />
          </div>
        </a-collapse-panel>
      </a-collapse>
    </div>
  </div>
</template>

<script>
import BarChart from "./Visualization/Bar.vue";
import BoxChart from "./Visualization/Box.vue";
import AreaChart from "./Visualization/Area.vue";
import ScatterChart from "./Visualization/Scatter.vue";
import MultiBarChart from "./Visualization/MultiBar.vue";
import ApiService from "../services/api-service";

export default {
  name: "Main",
  components: { BarChart, BoxChart, AreaChart, ScatterChart, MultiBarChart },
  data: () => ({
    csv: null,
    loaded: false,
    columns: [],
    csvFile: null,
    data: [],
    report: {},
    predictionLoading: false,
    predictions: null,
    predictionColumns: [],
    predictionsLoaded: false,
    activeKey: [],
    collapseStyle:
      "background: #f7f7f7;margin: 5px; border-radius: 4px;margin-bottom: 24px;border: 0;overflow: hidden; text-align: center; font-size: 20px"
  }),
  methods: {
    reset() {
      this.loaded = false;
      this.csv = null;
      this.csvFile = null;
      this.data = [];
      this.report = {};
      this.columns = [];
      this.activeKey = [];
      this.predictions = null;
      this.predictionColumns = [];
      this.predictionsLoaded = false;
      this.predictionLoading = false;
    },
    fetchCsv(e) {
      this.reset();
      if (window.FileReader) {
        const reader = new FileReader();
        this.csvFile = e.target.files[0];
        reader.readAsText(e.target.files[0]);
        reader.onload = event => (this.csv = event.target.result);
        reader.onerror = event => {
          if (event.target.error.name === "NotReadableError") {
            alert("Cannot read file !");
          }
          this.csvFile = null;
        };
      } else {
        alert("FileReader are not supported in this browser.");
      }
    },
    parseCsv() {
      if (this.loaded) return;
      const lines = this.csv.split("\n");
      let result = [];
      const headers = ["ID"].concat(lines[0].split(","));
      lines.forEach((line, indexLine) => {
        if (indexLine < 1) return;

        const obj = {};
        const currentLine = [indexLine].concat(line.split(","));
        headers.forEach(
          (header, indexHeader) => (obj[header] = currentLine[indexHeader])
        );
        result.push({ ...obj, key: indexLine });
      });
      result.pop();
      if (result.length > 50)
        return alert("Quote Exceeded, Max allowed size is 30.");
      this.columns = headers
        .filter(header => header !== "")
        .map(header => ({
          title: header,
          dataIndex: header,
          width: 100
        }));
      result.forEach(row => delete row[""]);
      this.data = result;
      this.loaded = true;
      this.activeKey = ["1", "2"];
    },
    async generatePredictions() {
      try {
        if (this.predictionsLoaded) return;
        this.predictionLoading = true;
        let {
          predictions,
          report
        } = await ApiService.generateDatasetPrediction(this.csvFile);
        let headers = Object.keys(predictions[0]).map(key => ({
          title: key.toUpperCase(),
          dataIndex: key,
          width: 100
        }));
        headers = [headers[1]].concat([headers[0], headers[2]]);
        predictions = predictions.map((prediction, i) => ({
          ...prediction,
          key: i + 1
        }));
        let correctCount = 0;
        predictions.forEach(prediction => {
          if (prediction.predicted === prediction.established)
            correctCount = correctCount + 1;
        });
        const accuracy = Number(
          Number((correctCount / predictions.length) * 100).toFixed(2)
        );
        this.predictionColumns = headers;
        this.predictions = predictions;
        this.report = report;
        this.predictionLoading = false;
        this.predictionsLoaded = true;
        this.$notification["success"]({
          message: "Prediction's Ready",
          duration: 10,
          description: `Our Model has evaluted your data with accruacy: ${accuracy}%`
        });
        this.activeKey = this.activeKey.concat("3");
      } catch (err) {
        console.error(err.message ? err.message : err);
        this.$notification["error"]({
          message: "Error During Inference",
          duration: 10,
          description:
            "Unknown error occured during the inference process.Check server logs for details."
        });
        this.predictionLoading = false;
      }
    }
  }
};
</script>

<style scoped>
.panel {
  border: 2px solid #dfdfdf;
  box-shadow: rgba(0, 0, 0, 0.15) 0 1px 0 0;
  margin: 5px;
}
.panel.panel-sm {
  max-width: 700px;
  margin: 10px auto;
}
img {
  width: 8%;
  height: 90px;
  margin: 10px;
}
</style>

// PrimeVue Imports
import DataTable from "primevue/datatable"
import Column from "primevue/column"
import ColumnGroup from "primevue/columngroup" // optional
import Row from "primevue/row"
import Chart from "primevue/chart"
import Toast from 'primevue/toast';

export default function setupPrimeVue(app) {
	app.component("DataTable", DataTable)
	app.component("Column", Column)
	app.component("ColumnGroup", ColumnGroup)
	app.component("Row", Row)
	app.component("Chart", Chart)
	app.component("Toast", Toast)
}

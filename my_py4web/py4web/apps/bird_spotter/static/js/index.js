"use strict";

function clone(obj) {
return JSON.parse(JSON.stringify(obj));
}

let app = {};
(app.empty_new_bird = {
id: 0,
name: "",
habitat: "",
weight: 0,
sightings: 0,
}),
(app.config = {
data: function () {
return {
new_bird: clone(app.empty_new_bird),
birds: [],
selected_birds: [],
editing: { current: null },
};
},
methods: {
search: function () {
this.cancel();
this.selected_birds = this.birds.filter((bird) => {
return bird.name
.toLowerCase()
.includes(this.new_bird.name.toLowerCase());
});
},
add_bird: function () {
this.cancel();
if (this.selected_birds.length == 0 && this.new_bird.name.length > 1) {
let bird = clone(this.new_bird);
this.birds.push(bird);
this.new_bird = app.empty_new_bird;
this.selected_birds = [bird];
// POST bird to /bird_spotter/birds which returns {id: #} and store it in bird.id = #;
fetch("../birds", {
method: "POST",
headers: {
"Content-Type": "application/json",
},
body: JSON.stringify(bird),
})
.then((response) => response.json())
.then((data) => {
bird.id = data.bird.id;
});
}
},
edit: function (bird) {
this.cancel();
this.editing = { current: bird, old: clone(bird) };
},
save: function (bird) {
let birdId = bird.id;
bird = clone(bird);
delete bird.id;
delete bird.name;
// PUT bird to /bird_spotter/birds/{bird.id}
fetch(`../birds/${birdId}`, {
method: "PUT",
headers: {
"Content-Type": "application/json",
},
body: JSON.stringify(bird),
});
this.editing = { current: null };
},
cancel: function () {
if (this.editing.current)
for (var key in this.editing.current)
this.editing.current[key] = this.editing.old[key];
this.editing = { current: null };
},
delete_bird: function (bird) {
this.cancel();
this.birds = this.birds.filter((b) => b.id != bird.id);
// DELETE /bird_spotter/birds/{bird.id}
fetch(`../birds/${bird.id}`, {
method: "DELETE",
});
},
add_sighting: function (bird) {
bird.sightings += 1;
// POST {} to /bird_spotter/birds/{bird.id}/increase_sightings
fetch(`../birds/${bird.id}/increase_sightings`, {
method: "POST",
});
},
color: function (name) {
let hash = 0;
for (let i = 0; i < name.length; i++)
hash = name.charCodeAt(i) + ((hash << 5) - hash);
let ret = `hsl(${hash % 360}, 100%, 75%)`;
console.log(ret);
return ret;
},
},
});
app.load_data = function () {
// GET from /bird_spotter/birds {birds: [...]} and store it into app.vue.birds = [...]
fetch("../birds")
.then((response) => response.json())
.then((data) => {
app.vue.birds = data.birds;
});
};

app.vue = Vue.createApp(app.config).mount("#app");
app.load_data();

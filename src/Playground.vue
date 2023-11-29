export default {
  components: {
    Toolbar,
  },
};
<script setup>
import Toolbar from './components/Toolbar.vue'
import ControlsToolbar from './components/ControlsToolbar.vue'
//import tone js
import * as Tone from 'tone'
</script>

<template>
    <header>
        <Toolbar @savepreset="savePreset" @loadpreset="loadPreset" />
        <!-- Your main content goes here -->
    </header>

    <main @contextmenu.prevent="setVisibleContextMenu($event)">
        <div class="mainDiv" @mousedown="clickedMainDiv($event, true)" @mouseup="clickedMainDiv($event, false)" @mousemove="moveMainDiv">
        <div style="cursor:default">
            <!-- create a module -->
            <!-- <Module :moduleName="moduleName" :inputPorts="inputPorts" :outputPorts="outputPorts"
                @start-dragging-port="startPortDragging" @handle-port-drag="handlePortDragging" @stop-dragging-port="stopPortDragging"/>
            -->
                <!--
        <img alt="Vue logo" class="logo" src="./assets/logo.svg" width="125" height="125" />
        <div class="wrapper">
        -->
            <div v-for="(module, index) in modules" :key="index">
                <Module :moduleName="module.moduleName" :inputPorts="module.inputPorts"
                    :outputPorts="module.outputPorts" :createdCoordsX="module.createdCoordsX"
                    :createdCoordsY="module.createdCoordsY" :moduleId="module.id"
                    :moduleType="module.type"
                    @contextmenu.prevent="setVisibleContextMenu($event)"
                    @module-moved="moduleMovedUpdate" @remove-module="removeModule"
                    :style="{
                    transform: 'translate(' + playGroundXtranslate + 'px,' + playGroundYtranslate +'px)' }"
                    >
                    <component :is="module.type" @portClicked="startPortDragging"  
                    @modulePortMouseMoved="handlePortDragging"
                    @modulePortMouseStopMove="stopPortDragging"
                    @modulePortHover="trackPort"
                    @modulePortOut="stopTrackPort"
                    ></component>
                </Module>
            </div>
        </div>

        <!-- Add more options as needed -->
        <!--
        <div v-if="contextMenuVisible" class="context-menu"
            :style="{ top: contextMenuPosition.y + 'px', left: contextMenuPosition.x + 'px' }">
            <div class="contextualMenuButton" @click="addModule('New Module', fromContextMenu = true)">Add Module</div> 
        -->

        <button id="libButton" class="libraryButton material-symbols-outlined" @click="libraryButtonClicked">arrow_forward_ios</button>
        <div id="modulesScaffold" v-if="libButtonClicked" class="modules-scaffold">
            <div class="scaffoldTitle"> MODULE SCAFFOLD </div>
            <!-- <div v-if="isDragging()"> heyyyyy </div>-->
        <!-- display all items from myJson -->
        <div v-for="(item,index) in mod_categories" :key="index">
            <!-- simply display its contents as text -->
            <div class="scaffoldCategory" :id="'category' + (index)" @click="toggleCategory(index)">
                {{ item.toLocaleUpperCase()}} <span class="material-symbols-outlined" 
                :id="'category_span' + (index)">arrow_drop_down</span></div>
            <!-- if the category is expanded then you need to showcase its content -->
            <!-- <div v-if="isExpanded(index)" class="scaffoldCategoryContent">
                {{("heyyy I'm category "+index)}}</div> -->
            <div v-if="isExpanded(index)" class="scaffoldCategoryContent">
                <!-- get the content from the synth info json-->
                <div v-for="(it, ind) in categories_content[index]" :key="ind" class="scaffoldCategoryItem" @click="addModule(it)">
                    <!-- recover from the same json it, then display 
                        the image associated to the field "preview_img_source" of the field it -->
                    <img :src="'./src/assets/images/' + it + '.png'" class="scaffoldCategoryItemImg">
                    {{it}}
                </div>
            </div>
        </div> 

        </div>
        <!-- demo clutter -->
         
        <svg class="visualConnections">
            <line v-if="(isDragging())" :x1="dragPortPositionX" :y1="dragPortPositionY" :x2="mouseCurrentX"
                :y2="mouseCurrentY" stroke="blue" stroke-width="2" />
        </svg>
    
        <svg class="visualConnections"  v-for="(item,index) in connections" :key="index">
            <line  :x1="(connections[index].x1 + playGroundXtranslate)" :y1="(connections[index].y1 + playGroundYtranslate)"
                :x2="(connections[index].x2 + playGroundXtranslate)" :y2="(connections[index].y2 + playGroundYtranslate)" :stroke="connections[index].color" stroke-width="6" />
        </svg>
        </div> <!--mainDiv-->
    </main>

    <div class="controls">
        <ControlsToolbar oncontextmenu="return false;" />
    </div>
</template>

<style scoped>
/* checkout https: //developers.google.com/fonts/docs/material_symbols */
header {
    line-height: 1.5;
}

html,
body {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
}

body {
    display: flex;
    flex-direction: column;
    background-color: rgb(202, 60, 60);
}

main {
    top:0;
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    /* background-color: rgb(128, 129, 150);  */ /*old colors #767779;*/
    background-color: rgb(52, 54, 64);
    /* a5a5a5ab old color */
    background-image: linear-gradient(90deg, #585858ab 2px, transparent 1px),
        linear-gradient(#585858ab 2px, transparent 1px);
    background-size: 30px 30px;/*square size*/
    
    min-height: 100%;
    min-width: 100%;
    overflow: hidden;
    flex-grow: 1;
    position: absolute;
    left: 0;
}

.logo {
    display: block;
    top: 10px;
    margin: 0 auto 2rem;
}

.mainDiv {
    user-select: none;
    background-color: transparent;
    min-height: 100%;
    min-width: 100%;
    overflow: hidden;
    flex-grow: 1;
    position: absolute;
    left: 0;
    cursor:grab;
}

.context-menu {
    position: absolute;
    z-index: 1000;
    background-color: #fff;
    border: 1px solid #111;
    /*make the text black*/
    color: #000;
    border-radius: 1px;
    cursor: pointer;
    margin: 5px;
    z-index:99;
}

.contextualMenuButton {
    padding: 10px;
    background-color: #fff;
    border: 1px solid #111;
    /*make the text black*/
    color: #000;
    border-radius: 1px;
    cursor: pointer;
    margin: 5px;
    transition: background-color 0.3s, color 0.3s;
}

.libraryButton {
    /* a button on mid of main that has a ">" inside.
  When clicked will open a section containing all modules*/
    position: absolute;
    top: 50%;
    left: 1%;
    background-color: #fff;
    border: 1px solid #111;
    /*make the text black*/
    z-index:101;
    transform: translate(0, -50%);
    background-color: rgba(199, 199, 199, 0);
        /* Blue background */
        border: none;
        /* Remove borders */
        color: white;
        /* White text */
        padding: 12px 16px;
        /* Some padding */
        font-size: 16px;
        /* Set a font size */
        cursor: pointer;
        /* Mouse pointer on hover */
    transition: transform 0.3s ease;
    font-size: 32px;
}

.libraryButton:hover {
    background-color: rgb(147, 64, 224);
    /* Blue background */
}

.contextualMenuButton:hover {
    background-color: rgb(105, 105, 105);
    color: #fff;
}

.modules-scaffold {
    user-select: none;
    position: absolute;
    top: 3.45rem;
    left: 0;
    width: 25%;
    /* make this extend for all height */
    bottom: 2.2em;
    background-color: rgb(255, 255, 255);
    /*add a black border*/
    border: 1px solid #111;
    z-index: 1202;
    transition: width 0.3s ease;
    overflow: scroll;
    cursor: default;
}

.modules-scaffold.active {
    width: 30%;
}

.scaffoldTitle{
    font-size: 1.5rem;
    font-weight: bold;
    text-align: center;
    padding: 1rem;
    background:#111;
    color:#fff;
    font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
}

.scaffoldCategory{
    display: flex;
    flex-direction:row;

    justify-content: space-between;
    align-items: center;
    padding: 5px;
    border: 1px solid #ccc;
    cursor: pointer;
    background-color: rgb(255, 255, 255);
}
.scaffoldCategory:hover{
    background-color: rgb(105, 105, 105);
    color: #fff;
}
.scaffoldCategoryContent{
    display:flex;
    flex-direction:row;
}
.scaffoldCategoryItem{
    /* display items in a column */
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 5px;
    border: 1px solid #ccc;
    cursor: pointer;
}

.visualConnections{
    z-index:1201;
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
}
.playgroundBG{
    cursor: grab;
}

.maindiv-grabbed{
    cursor: grabbing;
}

@media (min-width: 1024px) {
    header {
        display: flex;
        place-items: center;
        padding-right: calc(var(--section-gap) / 2);
    }

    /*
  .logo {
    margin: 0 2rem 0 0;
  }
*/
    header .wrapper {
        display: flex;
        place-items: flex-start;
        flex-wrap: wrap;
    }
}
</style>
<script>
import Module from './components/Module.vue'
import BasicOsc from './components/synth_modules/BasicOsc.vue'
import AudioOut from './components/synth_modules/AudioOut.vue'
import MidiIn from './components/synth_modules/MidiIn.vue'
import Theremin from './components/synth_modules/Theremin.vue'
import Reverb from './components/synth_modules/Reverb.vue'
import VCA from './components/synth_modules/VCA.vue'
import Filter from './components/synth_modules/Filter.vue'

import ModuleConnection from './scripts/classes/ModuleConnection'
import list_json from './assets/synth_modules_list.json'
import synth_info_json from './assets/synth_modules.json'
import './scripts/utils/cycle.js'
export default {
    inject: ['ACM'],
    components: {
        Module,
        BasicOsc,
        AudioOut,
        MidiIn,
        Theremin,
        Reverb,
        VCA,
        Filter,
    },
    data() {
        return {
            libButtonClicked: false,
            contextMenuVisible: false,
            contextMenuPosition: { x: 0, y: 0 },
            modules: [],
            moduleName: "My Module",
            myJson: list_json,
            synth_info: synth_info_json,
            mod_categories: list_json["categories"],
            categories_content: synth_info_json["categories_content"],
            expandedCategories: [], //array of expanded categories ids
            connections: [], //save all connections between modules here
            isDraggingPort:false,
            dragPortPositionX:0,
            dragPortPositionY:0,
            mouseCurrentX:0,
            mouseCurrentY:0,
            makeConnectionPermanent:false,
            lastHoveredPortModID:-1,
            lastHoveredPortID:-1,
            lastHoveredPortX:0,
            lastHoveredPortY:0,
            lastAssignedModuleId:-1,


            canMovePlayground:false,
            playGroundMoveInitialX:0,
            playGroundMoveInitialY:0,
            playGroundXtranslate:0,
            playGroundYtranslate:0,
        };
    },
    options: {
        isDragging() {
            return this.isDraggingPort;
        },
    },
    methods: {
        isDragging(){
            return this.isDraggingPort;
        },
        startPortDragging(module, port, posX, posY) {
            // Implement the logic to handle port dragging here
            this.dragPortPositionX = posX;
            this.dragPortPositionY = posY;
            this.isDraggingPort = true;
            console.log("Starting")
            console.log(this.dragPortPositionX, this.dragPortPositionY)
        },
        handlePortDragging(posX, posY) {
            console.log("handling")
            if(!this.isDraggingPort){
                return;
            }
            //TODO: this is just an easy fix to the fact
            //the event listener is never remoevd and i was sick
            //of seeing the console spammed
            /*
            if(!this.isDragging()){
                return;
            }*/
            this.mouseCurrentX = posX;
            this.mouseCurrentY = posY;
            //make a line between posX, posY and the current mouse position
        },
        stopPortDragging(moduleID,portID,fromX,fromY) {
            this.isDraggingPort = false;
            //if you're over another port then guess what we're connecting the two
            //if you're not over another port then guess what we're not connecting the two
            //connecting = making the connection permanently visible
            
            //this.makeConnectionPermanent = true; //for demo purposes

            //for now this is quite useless
            console.log("Module ID from: ", moduleID)
            console.log("Last Hoevered module:", this.lastHoveredPortModID)
            console.log(this.isHoveringPort);
            if(this.isHoveringPort){
                if(moduleID != this.lastHoveredPortModID){
                    console.log("fff", moduleID, this.lastHoveredPortModID);
                    //let connection = new ModuleConnection(this.ACM, moduleID, this.lastHoveredPortModID, portID, this.lastHoveredPortID, fromX, fromY, this.lastHoveredPortX, this.lastHoveredPortY);
                    //here one could check if the connection is valid and makes sense, 
                    //however, taking inspiration from VCV rack, we decided it really 
                    //doesn't make sense to do that
                    //and we'd rather let the user take weird decisions
                    let valid = this.ACM.checkConnectionValidity(moduleID, this.lastHoveredPortModID, portID, this.lastHoveredPortID);
                    if (valid){
                        this.connections.push(new ModuleConnection(this.ACM, moduleID, this.lastHoveredPortModID, 
                        portID, this.lastHoveredPortID, fromX - this.playGroundXtranslate, 
                        fromY - this.playGroundYtranslate, this.lastHoveredPortX - this.playGroundXtranslate, 
                        this.lastHoveredPortY - this.playGroundYtranslate));
                        this.connections[this.connections.length - 1].printConnection();
                    }else{
                        console.log("Invalid connection");
                    }
                }
            }
            this.isHoveringPort = false;
        },
        

        trackPort(moduleId, portID, x, y){
            //console.log(moduleId, portID, x, y);
            this.lastHoveredPortModID = moduleId;
            this.lastHoveredPortID = portID;
            this.lastHoveredPortX = x;
            this.lastHoveredPortY = y;
            this.isHoveringPort = true;
        },
        stopTrackPort(){
            this.isHoveringPort = false;
        },

        moduleMovedUpdate(moduleId, xoff, yoff){
            //update all connections to and from this module to
            //match the new position
            this.findUpdateConnectionsToModule(moduleId, xoff, yoff);
            this.findUpdateConnectionsFromModule(moduleId, xoff, yoff);
        }, 
        findUpdateConnectionsToModule(moduleId,xoff,yoff){
            if (this.connections.length == 0){
                return;
            }
            for (let i = 0; i < this.connections.length; i++) {
                if (this.connections[i].toId == moduleId) {
                    this.connections[i].x2 += xoff;
                    this.connections[i].y2 += yoff;
                }
            }
        },
        findUpdateConnectionsFromModule(moduleId, xoff, yoff){
            if (this.connections.length == 0) {
                return;
            }
            for(let i = 0; i < this.connections.length; i++){
                if (this.connections[i].fromId == moduleId){
                    this.connections[i].x1 += xoff;
                    this.connections[i].y1 += yoff;
                }
            }
        },
        removeConnectionsWithModule(moduleId){
            if (this.connections.length == 0) {
                return;
            }
            for (let i = 0; i < this.connections.length; i++) {
                if (this.connections[i].fromId == moduleId || this.connections[i].toId == moduleId) {
                    this.connections.splice(i, 1);
                }
            }
        },
        removeModule(moduleId){
            //remove all connections to and from this module
            this.removeConnectionsWithModule(moduleId);
            this.ACM.removeNode(moduleId);
            //remove the module itself
            for(let i = 0 ; i < this.modules.length; i++){
                if (this.modules[i].id == moduleId){
                    this.modules.splice(i, 1);
                }
            }
        },

        setVisibleContextMenu(event) {
            console.log(this.contextMenuVisible)
            if (this.contextMenuVisible == true) {
                //console.log("Hi")
                this.contextMenuVisible = false;
            } else {
                this.contextMenuVisible = true;
                this.contextMenuPosition = { x: event.clientX, y: event.clientY };
                //console.log(event.clientX, event.clientY)
            }
            //console.log(Boolean(event.originalTarget.closest("modulesScaffold")))
            if (event.target.parentElement.classList.contains("module")){
                //manage the removal of modules here
            }
            console.log(event);
        },
        addModule(moduleName, fromContextMenu = false) {
            // Add a new module to the modules array
            if(!fromContextMenu){
                let codeName = synth_info_json[moduleName]["codename"];
                //let currId = this.modules.length;
                let currId = this.lastAssignedModuleId + 1;
                this.lastAssignedModuleId = currId;
                //just have it in a random (visible hopefully) position
                this.modules.push({
                    moduleName,
                    type: codeName,
                    id: currId,
                    /*
                    inputPorts: [
                        { id: 1, x: 10, y: 50 },
                        { id: 2, x: 10, y: 80 },
                    ], // Define initial input ports if needed
                    outputPorts: [
                        { id: 1, x: 190, y: 50 },
                        { id: 2, x: 190, y: 80 },
                    ], // Define initial output ports if needed
                    */
                    createdCoordsX: (Math.floor(Math.random()*600)+200) - this.playGroundXtranslate,
                    createdCoordsY: (Math.floor(Math.random() * 500)+100) - this.playGroundYtranslate,
                });
                return;
            }
            //add a module at the position of the context menu
            this.modules.push({
                moduleName,
                inputPorts: [
                    { id: 1, x: 10, y: 50 },
                    { id: 2, x: 10, y: 80 },
                ], // Define initial input ports if needed
                outputPorts: [
                    { id: 1, x: 190, y: 50 },
                    { id: 2, x: 190, y: 80 },
                ], // Define initial output ports if needed
                createdCoordsX: this.contextMenuPosition.x,
                createdCoordsY: this.contextMenuPosition.y,
            });
            //console.log("POS: "+this.contextMenuPosition.x + "   " + this.contextMenuPosition.y)
            // Close the context menu
            this.contextMenuVisible = false;
        },


        libraryButtonClicked() {
            this.libButtonClicked = !this.libButtonClicked;
            if (this.libButtonClicked) {
                //document.getElementById("libButton").style.left = "10%";
                document.getElementById("libButton").style.transform = "translate(calc(24cqw), -50%) ";
                document.getElementById("libButton").innerHTML = "arrow_back_ios_new";
                //document.getElementById("libButton").style.transform = "rotate(180deg)";
                //get the modulesScaffold and make a transition from 0 width to 300 px width
                //document.getElementById("modulesScaffold").classList.add("active");
                //console.log(document.getElementById("modulesScaffold")) //it doesnt exist yet here!
            }
            else {
                //document.getElementById("libButton").style.left = "1%";
                document.getElementById("libButton").innerHTML = "arrow_forward_ios";
                document.getElementById("libButton").style.transform = "translate(0px, -50%)";
            }   
        },

        toggleCategory(index) {
            // Toggle the expanded state of the category at the given index
            if (this.expandedCategories.includes(index)) {
                this.expandedCategories = this.expandedCategories.filter(i => i !== index);
                document.getElementById("category_span" + index).innerHTML = "arrow_drop_down";
            } else {
                this.expandedCategories.push(index);
                document.getElementById("category_span" + index).innerHTML = "arrow_drop_up";
            }
        },
        isExpanded(index) {
            return this.expandedCategories.includes(index);
        },

        /* //testing function, should you wish to test the ACM alone
        play() {
            const synth = new Tone.Synth().toDestination();
            synth.triggerAttackRelease("C4", "2n");
            console.log("lol");
            this.ACM.testACM()
        },
        */


        //PLAYGROUND MOVEMENT STUFF
        clickedMainDiv(event, type){
            //if the class of the event original target is not mainDiv
            //then do nothing
            console.log(event)
            if (event.target.classList.contains("mainDiv") == false){
                //console.log("non duce")
                return;
            }
            //console.log("duce")
            this.canMovePlayground = type; //type is a boolean
            if (type == true){
                //
                event.target.classList.add("maindiv-grabbed")
                this.playGroundMoveInitialX = event.clientX;
                this.playGroundMoveInitialY = event.clientY;
            }
            else{
                //
                event.target.classList.remove("maindiv-grabbed")
            }

        },
        moveMainDiv(event){
            //i'm sure this won't be a problem at all
            //and won't hog resources for nothing
            //...however time is short
            if(this.canMovePlayground == false){
                return;
            }
            console.log(event.clientX, event.clientY)
            console.log("moving the playground sire!")
            this.playGroundXtranslate += event.clientX - this.playGroundMoveInitialX;
            this.playGroundYtranslate += event.clientY - this.playGroundMoveInitialY;
            this.playGroundMoveInitialX = event.clientX;
            this.playGroundMoveInitialY = event.clientY;
        },


        //PRESET MANAGEMENT STUFF
        async savePreset(){
            console.log("saving preset!!!!")
            //create a small screen to get user input
            //get the name of the preset
            
            //create the small screen
            let presetName = prompt("Please enter the name of your preset", "Preset Name");
            if (presetName == null || presetName == ""){
                return;
            }
            
            //create a new preset object
            let METADATA = {
                "preset_name": presetName,
                "creator_id": 0, //get the current user's id from the local storage,
                "public": true// if trueeverybody who has the preset_id can edit it
            }
            let PLAYGROUND_STATE = {
                "x": this.playGroundXtranslate,
                "y": this.playGroundYtranslate,
                "modules": this.modules,
                "connections": this.connections,
                "lastAssignedModuleId": this.lastAssignedModuleId
            }; //we need a specific functions for modules
            //to get their state. Both from module.vue and from the ACM
            let ACM_DATA = this.ACM.getData();

            let DATA = { "playground_data": PLAYGROUND_STATE, "ACM_data": ACM_DATA };
            let preset = {
                "metadata":METADATA,
                "data": DATA
            }

            //save this on the goofy ahh database
            
            //TODO
            var data = JSON.stringify({
                "preset": JSON.decycle(preset)
            });
            console.log(data);
            fetch('http://localhost:5000/presets/new', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: data,
            })
                .then(response => response.json())
                .then(data => {
                    console.log('Success:', data);
                })
                .catch((error) => {
                    console.error('Error:', error);
                });
        },

        loadPreset(){
            console.log("loading preset!!!!")
            //load the preset from the database

            //empty modules and connections in case there is any

            //re-initialise ACM if needed

        },
    },

};
</script>
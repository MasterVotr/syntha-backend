
<script>
export default {
    inject: ['ACM'],
    props: {
        moduleName: String, // The name of the module
        moduleType: String,
        /*
        inputPorts: Array, // An array of input ports (objects with id, x, y)
        outputPorts: Array, // An array of output ports (objects with id, x, y)
        */
        createdCoordsX: Number,
        createdCoordsY: Number,
        moduleId: Number,
    },
    created(){
        this.createdCoords = [this.createdCoordsX, this.createdCoordsY]
        this.currentPosition = {
            x: this.createdCoordsX,
            y: this.createdCoordsY,
        };
        this.startPosition = {
            x: this.createdCoordsX,
            y: this.createdCoordsY,
        };
        this.lastPosition = {
            x: this.currentPosition.x,
            y: this.currentPosition.y,
        };
    },
    mounted(){
        this.ACM.addNode(this.moduleId, this.moduleType);
    },
    data() {
        return {
            isDragging: false,
            startPosition: { x: 0, y: 0 },
            currentPosition: { x: 0, y: 0 },
        };
    },
    computed: {
        elementStyles() {
            return {
                top: `${this.currentPosition.y}px`,
                left: `${this.currentPosition.x}px`,
                //transform: `translate(${this.currentPosition.x}px, ${this.currentPosition.y}px)`,
            };
        },
    },
    methods: {
        /*
        //goofy aah code from the demo gala
        startDraggingPort(port, event) {
            // Implement the logic to start dragging the port
            // You can use Vue's $emit to notify the parent component
            // that a port is being dragged
            console.log("this is atest")
            console.log(this.currentPosition);
            //this.$emit('start-dragging-port', port, event.clientX - this.currentPosition.x, event.clientY - this.currentPosition.y);
            this.$emit('start-dragging-port', port, event.clientX , event.clientY);
            
            
            //window.addEventListener("mousemove", this.handlePortDrag(port, event));
            //window.addEventListener("mouseup", this.stopDraggingPort(port));
            
            
            window.addEventListener("mousemove", (e) => this.handlePortDrag(e));
            window.addEventListener("mouseup", (e) => this.stopPortDrag(port, e));
        },
        stopPortDrag(port, event){
            this.$emit('stop-dragging-port', port, event.clientX, event.clientY);
            window.removeEventListener("mousemove", this.handlePortDrag);
            window.removeEventListener("mouseup", this.stopDraggingPort);
        },
        handlePortDrag(event){
            this.$emit('handle-port-drag', event.clientX, event.clientY);
        },
        */
        startDragging(event) {
            //if control is pressed return
            if (event.ctrlKey) {
                return;
            }
            this.isDragging = true;
            this.startPosition = {
                x: event.clientX - this.currentPosition.x,
                y: event.clientY - this.currentPosition.y,
            };
            window.addEventListener("mousemove", this.handleDrag);
            window.addEventListener("mouseup", this.stopDragging);
        },
        handleDrag(event) {
            if (this.isDragging) {
                this.currentPosition = {
                    x: event.clientX - this.startPosition.x,
                    y: event.clientY - this.startPosition.y,
                };
                let offSetX = this.currentPosition.x - this.lastPosition.x;
                let offSetY = this.currentPosition.y - this.lastPosition.y;
                this.$emit('module-moved', this.moduleId, 
                    offSetX, offSetY
                );
                
                this.lastPosition = {
                    x: this.currentPosition.x,
                    y: this.currentPosition.y,
                };
                
                
            }
        },
        stopDragging() {
            this.isDragging = false;
            window.removeEventListener("mousemove", this.handleDrag);
            window.removeEventListener("mouseup", this.stopDragging);
        },
        
        handleModulePortClick(){
            console.log("module port clicked and passed");
        },
        removeModule(){
            this.$emit('remove-module', this.moduleId);
            var event = new Event("remove-module-"+this.moduleId);
            // Dispatch the event.
            dispatchEvent(event);
        },
        test(){
            console.log("test");
        },
    },
};
</script>

<template>
<div class="module" :style="elementStyles">
    <div class="module-title" @mousedown="startDragging">{{ moduleName }} <a style="cursor:pointer" @click="removeModule"> &nbsp;&nbsp;&nbsp;&nbsp;X </a></div>
    <div class="module-control-area">
        <slot></slot> <!-- <slot/> -->
        
        <!-- 
            <div class="input-ports">-->
                <!-- careful! Numbering starts from 1 here -->
                <!--
                    <div class="input-port" v-for="inputPort in inputPorts" :key="inputPort.id" v-bind:id="'inputPort'+inputPort.id"
                    @mousedown="startDraggingPort(inputPort, $event)"></div>
                </div>
                <div class="output-ports">
                    <div class="output-port" v-for="outputPort in outputPorts" :key="outputPort.id"
                    @mousedown="startDraggingPort(outputPort, $event)"></div>
                </div>
            -->
        </div>
    </div>
</template>

<style scoped>
    .module {
        /*
        width: 400px;
        height: 150px;
        */
        
        width: fit-content;
        height: fit-content;
        
        min-width: 100px;
        min-height: 100px;
        
        background-color: #ccc;
        border: 1px solid #000;
        position: absolute;
        display: flex;
        flex-direction: column;
        
    }
    
    .module-title {
        user-select: none;
        background-color: #000;
        color: #fff;
        padding: 0px;
        height: 25px;
        width: 100%;
        align-items: center;
        text-align: center;
        cursor: move;
    }
    
    .module-knobs {
        margin-top: 10px;
    }
    
    .module-control-area {
        /*
        display: flex;
        position:relative;
        top:0%;
        left:0%;
        */
        top:25px;
        width: 100%;
        height:100%;
        min-height:100px;
        
    }
    
    .input-ports,
    .output-ports {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    
    .input-port,
    .output-port {
        width: 15px;
        height: 15px;
        background-color: #fff;
        border: 1px solid #000;
        border-radius: 50%;
        margin: 5px;
        cursor: pointer;
    }
</style>
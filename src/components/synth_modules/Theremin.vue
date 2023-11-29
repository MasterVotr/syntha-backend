//horizontal: pitch
//vertical: amplitude
<template>
    <div class="mainDivThe">
        <div class="thereminControlArea"  @mousedown="setMovable($event,true)" @mouseup="setMovable($event,false)" @mousemove="handleThereminMouseOver">
        <div class="theremin-indicator" 
        :style="{ top: thereminIndicator.y + 'px', left: thereminIndicator.x + 'px' }">
        </div>
        </div>
        <div class="theremin-indications">
            Vertical axis: amplitude
            <br>
            Horizontal axis: pitch
            <br> 
            Click and drag to move! 
            <br>
            (just clicking won't update values!)
        </div>
        <div class="portContainerThe">
            <component @portClicked="handlePortClick" @portMouseMoved="handlePortMouseMove"
                @portMouseStopMove="handlePortMouseStopMove" @portHovered="handlePortHover" @portOut="handlePortOut"
                :is="'Port'" :type="'OUT'" :parameter="'OUT'" :modId="this.$parent.moduleId" :ID="0"></component>
        </div>
    </div>
</template>

<style>
.mainDivThe {
    position: relative;
    display: flex;
    flex-direction: column;
    top: 0%;
    left: 0%;
    width: 100%;
    height: 100%;
    min-height: 390px;
    min-width: 300px;
    background-color: rgb(24, 24, 24);
    overflow: hidden;
}
.thereminControlArea{
    position: absolute;
    top: 0%;
    left: 0%;
    width: 100%;
    height: 300px;
    background-color: transparent;
    overflow: hidden;
}

.portContainerThe {
    position: absolute;
    top: 300px;
    left: 0%;
    width: 100%;
    border: 1px solid white;
    height: 90px;
    transform: translate(0,0);
    background-color: rgb(24, 24, 24);
}

.theremin-indicator {
    /* it's just a circle lol */
    position: absolute;
    width: 5%;
    height: 5%;
    transform: translate(-50%, -50%);

    border-radius: 50%;

    background-color: rgb(255, 255, 255);
}

.theremin-indications{
    color: indianred;
}
</style>
<script>
import Knob from '../functional/Knob.vue';
import Port from '../functional/Port.vue';
import { mapValue } from "../../scripts/utils/utils.js"
export default {
    inject: ['ACM'],
    components: {
        Knob,
        Port,
    },
    created() {

    },
    data(){
        return{
            thereminIndicator: {
                x: 0,
                y: 0,
            },
            movable: false,
        }
    },
    methods: {
        setMovable(event, flag){
            this.movable=flag;
            if(flag){
                this.thereminIndicator.x = event.layerX;
                this.thereminIndicator.y = event.layerY;
            }
        },
        handleThereminMouseOver(event){
            if(!this.movable){
                return;
            }
            //thanks random guy from stackoverflow
            //this was a pain in the ass to code
            var rect = event.target.getBoundingClientRect();
            this.thereminIndicator.x = event.pageX - rect.left;
            this.thereminIndicator.y = event.pageY - rect.top;
            if(this.thereminIndicator.y >300){
                this.thereminIndicator.y = 300;
            }
            //a quick google search told me that the theremin covers approximately
            //from C2 to C7 (5 octaves)
            //using https://pages.mtu.edu/~suits/notefreqs.html for tunings
            let freqVal = mapValue(this.thereminIndicator.x, 0, 300, 65.41, 2093)
            let volumeVal = ( 1 - mapValue(this.thereminIndicator.y, 0, 300,0, 1))
            //this conversion to decibel doesn't make any sense, I'm just going by ear
            volumeVal = 30 * Math.log10(volumeVal) 
            this.ACM.updateModuleParameter(this.$parent.moduleId, "frequency", freqVal);
            this.ACM.updateModuleParameter(this.$parent.moduleId, "volume", volumeVal)

        },

        //PORT FUNCTIONS (EVERY MODULE NEEDS TO HAVE THESE!)
        handlePortClick(portID, x, y) {
            console.log("parent", this.$parent.moduleId)
            console.log(this.$parent)
            this.$emit("portClicked", this.$parent.moduleId, portID, x, y);
        },

        handlePortMouseMove(x, y) {
            this.$emit("modulePortMouseMoved", x, y);
        },

        handlePortMouseStopMove(modId, portID, x, y) {
            console.log("stopped moving ", modId)
            this.$emit("modulePortMouseStopMove", modId, portID, x, y);
        },
        handlePortHover(portID, x, y) {
            this.$emit("modulePortHover", this.$parent.moduleId, portID, x, y);
        },
        handlePortOut(portId) {
            this.$emit("modulePortOut", this.$parent.moduleId, portId)
        },
    },
}
</script>
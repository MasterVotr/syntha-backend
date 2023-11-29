<template>
    <div class="container" 
    @mouseover="handlePortMouseOver"
    @mouseout="handlePortMouseOut" 
    @mousedown="handlePortMouseClick">
    <div class="square" :style="{ backgroundColor: squareColor }"
    >
        <div class="circle" :style="{ backgroundColor: circleColor, borderColor: circleBorderColor }">
            <div class="innerCircle" :id="(this.circleRef || generateDefaultRef)" :ref="this.circleRef || generateDefaultRef"></div>
        </div>
    </div>
    </div>
<div class="portName">{{parameter}}</div>
</template>

<script>
export default {
    emits: {
        portClicked: null,
        portMouseMoved:null,
        portMouseStopMove:null,
        portHovered:null,
        portOut:null,
    },
    props: {
        parameter: String,
        type: String,
        ID: Number,
        modId: Number,
    },
    data() {
        return {
            portType: "OUT", // Default value
            normalColor: "rgb(255, 255, 255)",
            hoverColor: "rgb(255, 255, 255)",
            circleColor: "rgb(150,150, 150)",
            circleBorderColor: "rgb(255, 255, 255)",
            squareColor: "rgb(255, 255, 255)",
            portID: 0,
        };
    },
    created() {
        this.portType = this.type;
        if (this.portType === "IN") {
            this.normalColor = "rgb(0, 0, 0)";
            this.hoverColor = "rgb(75, 75, 75)";
        } else {
            this.normalColor = "rgb(220, 220, 220)";
            this.hoverColor = "rgb(170, 170, 170)";
        }
        this.squareColor = this.normalColor;
        if(this.ID != null)
        this.portID = this.ID;
        this.parentModuleID = this.modId; 
        this.circleRef = "innerCircle" + this.parentModuleID + this.portID;
    },
    computed: {
        generateDefaultRef() {
            // Generate the default ref based on your criteria
            return "innerCircle" + this.parentModuleID + this.portID; 
        },
    },
    methods:{
        handlePortMouseOver(){
            this.squareColor = this.hoverColor;
            //we only wish to handle this if the port accepts inputs
            if (this.portType == "IN") {
                //const innerCircle = this.$refs[this.circleRef];
                const innerCircle = document.getElementById(this.circleRef);
                const rect = innerCircle.getBoundingClientRect();

                // Calculate the center position
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;

                //event.clientX, event.clientY
                this.$emit("portHovered", this.portID, centerX, centerY);
            }
        },
        handlePortMouseOut(){
            this.squareColor = this.normalColor;
            this.$emit("portOut", this.portID);
        },
        handlePortMouseClick(event){
            //connections go from OUT to IN ports ONLY
            if(this.portType=="OUT"){
                //const innerCircle = this.$refs[this.circleRef];
                const innerCircle = document.getElementById(this.circleRef);
                const rect = innerCircle.getBoundingClientRect();
                // Calculate the center position
                const centerX = rect.left + rect.width / 2;
                const centerY = rect.top + rect.height / 2;
                
                //event.clientX, event.clientY
                this.$emit("portClicked", this.portID, centerX, centerY);
                
                window.addEventListener("mousemove", this.handlePortMouseMove);
                window.addEventListener("mouseup", this.handlePortStopMove);
            }
        },
        handlePortMouseMove(event){
            console.log("aaaa")
            this.$emit("portMouseMoved", event.clientX, event.clientY);
        },
        handlePortStopMove(event) {
            //console.log(event.target)
            //console.log("-----ref-----", this.$refs[this.circleRef])
            //const innerCircle = this.$refs[this.circleRef];
            const innerCircle = document.getElementById(this.circleRef);
            //console.log(innerCircle)
            const rect = innerCircle.getBoundingClientRect();

            // Calculate the center position
            const centerX = rect.left + rect.width / 2;
            const centerY = rect.top + rect.height / 2;
            this.$emit("portMouseStopMove",this.modId, this.portID, centerX, centerY);
            window.removeEventListener("mousemove", this.handlePortMouseMove);
            window.removeEventListener("mouseup", this.handlePortStopMove);
        },
        handlePortMouseUp() {
            console.log("mouseup!")
            
        }
    }
};
</script>

<style scoped>
.container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 60px;
    cursor: grab;
}

.container:active{
    cursor: grabbing;
}
.square {
    width: 50px;
    height: 50px;
    position: relative;
}

.circle {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}
.innerCircle {
    width: 30px;
    height: 30px;
    background-color: black;
    border-radius: 50%;
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
}

.circle:hover {
    border: 4px solid white;
}

.portName{
    text-align: center;
    font-size: 16px;
    color: #fff;
    font-weight: 600;
    text-shadow: 0px 0px 2px #000;
}
</style>

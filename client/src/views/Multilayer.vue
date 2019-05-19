<template>
  <div id="Multilayer" ref="Multilayer">
  </div>
</template>
<script>
  import * as d3 from "d3";
  import * as dat from "dat.gui";
  import * as THREE from 'three';
  import TrackballControls from 'three-trackballcontrols';
  import OrbitControls from 'three-orbitcontrols';
  import {CSS2DRenderer, CSS2DObject} from 'three-css2drender';

  export default {
    data() {
      return {
        fov: 45,
        near: 1,
        far: 100000,
        width: 0,
        height: 0,
        flag: true,
        state: [],
        opacity: 50,
        animateId: 0
      }

    },
    mounted() {
      this.webglInit();
      this.webgl();
      this.animate();
      this.guiInit();
    },
    beforeDestroy() {
      // console.log('删除');
      cancelAnimationFrame(this.animateId)
      self.camera = null,
        self.scene = null ,
        self.controls = null ,
        self.renderer = null,
        self.raycaster = null,
        self.mouse = null,
        self.InterSelected = null,
        self.light = null,
        self.labelRenderer = null,
        self.plane = null,
        self.commonNodes = null;
    },
    methods: {
      webglInit() {
        let self = this;
        self.camera = null,
          self.scene = null ,
          self.controls = null ,
          self.renderer = null,
          self.raycaster = null,
          self.mouse = null,
          self.InterSelected = null,
          self.light = null,
          self.color = this.getColor(),
          self.labelRenderer = null,
          self.plane = [],
          self.commonNodes = [];

        self.mouse = new THREE.Vector2();
        self.raycaster = new THREE.Raycaster();

        self.width = self.$refs.Multilayer.offsetWidth;
        self.height = self.$refs.Multilayer.offsetHeight;
        // 创建场景
        self.scene = new THREE.Scene();
        // 初始化相机
        self.camera = new THREE.PerspectiveCamera(self.fov, self.width / self.height, self.near, self.far);   //创建摄像机
        self.camera.up = new THREE.Vector3(0, 1, 0); // 设置y轴向上
        self.camera.layers.enable(0);
        self.camera.layers.enable(1);
        self.camera.layers.enable(2);
        self.camera.layers.enable(3);
        self.camera.position.z = 2299;
        self.camera.position.x = 0;
        self.camera.position.y = 0;
        self.camera.lookAt(self.scene.position);


        self.light = new THREE.AmbientLight(0xffffff);
        self.light.position.set(1, 1, 1);
        self.light.layers.enable(0);
        self.light.layers.enable(1);
        self.light.layers.enable(2);
        self.light.layers.enable(3);
        self.scene.add(self.light);


        // 渲染器  使用WebGL渲染器  同时还支持canvas svg
        self.renderer = new THREE.WebGLRenderer({
          antialias: true
        });
        self.renderer.setClearColor(new THREE.Color(0x303030));
        self.renderer.setSize(self.width, self.height);
        self.renderer.setPixelRatio(window.devicePixelRatio);
        document.getElementById("Multilayer").appendChild(self.renderer.domElement);

        // label渲染器
        self.labelRenderer = new CSS2DRenderer();
        self.labelRenderer.setSize(self.width, self.height);
        self.labelRenderer.domElement.style.position = 'absolute';
        self.labelRenderer.domElement.style.top = 0;
        document.getElementById("Multilayer").appendChild(self.labelRenderer.domElement);

        // 初始化控制器
        self.controls = new TrackballControls(self.camera, self.$refs.Multilayer);
        self.controls.rotateSpeed = 2.5;
        self.controls.zoomSpeed = 1.2;
        self.controls.panSpeed = 0.8;
        self.controls.noZoom = false;
        self.controls.noPan = false;
        self.controls.staticMoving = true;
        self.controls.dynamicDampingFactor = 0.3;


        window.addEventListener('resize', self.onWindowResize, false);
        document.getElementById("Multilayer").addEventListener('mousemove', self.onDocumentMouseMove, false);
      },
      webgl() {
        let self = this;
        self.flag = true;
        self.state[0] = false;
        self.state[1] = false;
        self.state[2] = false;
        self.scene.children = self.scene.children.slice(0, 1);
        $(".labelDiv").remove();

        let Url = "get-layout-data";
        let paramsObj1 = {
          layout_type: 'rt_circular',
          network_level: 3
        };
        let formData1 = new URLSearchParams();
        formData1.append("params", JSON.stringify(paramsObj1));
        self.getData(Url, formData1, 0, 1000, '链路');


        let paramsObj2 = {
          layout_type: 'rt_circular',
          network_level: 2
        };
        let formData2 = new URLSearchParams();
        formData2.append("params", JSON.stringify(paramsObj2));
        self.getData(Url, formData2, 1, 1000, '网络');

        let paramsObj3 = {
          layout_type: 'rt_circular',
          network_level: 3
        };
        let formData3 = new URLSearchParams();
        formData3.append("params", JSON.stringify(paramsObj3));
        self.getData(Url, formData3, 2, 1000, '应用');


      },
      getData(Url, formData, index, widthx, content) {
        let self = this;
        self.$api.get(Url, formData, data => {
          self.addObj(data, index, widthx, content);
          let xscale = d3.scaleLinear()
            .domain(d3.extent(data.nodes, d => d.x))
            .range([-widthx / 2 + 30, widthx / 2 - 30]);
          let yscale = d3.scaleLinear()
            .domain(d3.extent(data.nodes, d => d.y))
            .range([-widthx / 2 + 30, widthx / 2 - 30]);

          let nodes = [];
          for (let i = 0; i < 4; i++) {
            let random = Math.floor(Math.random() * data.nodes.length);
            nodes.push({'x': xscale(data.nodes[random].x), 'y': yscale(data.nodes[random].y)});
          }
          self[`level${index}`] = nodes;
          self.state[index] = true;
        }, error => {
          console.log('fail');
        })
      },
      addObj(data, index, widthx, content) {
        let self = this;
        let xscale = d3.scaleLinear()
          .domain(d3.extent(data.nodes, d => d.x))
          .range([-widthx / 2 + 30, widthx / 2 - 30]);
        let yscale = d3.scaleLinear()
          .domain(d3.extent(data.nodes, d => d.y))
          .range([-widthx / 2 + 30, widthx / 2 - 30]);

        // 添加圆
        let geometrySphere = new THREE.SphereGeometry(5, 5, 10);
        data.nodes.forEach(item => {
          let circle = new THREE.Mesh(geometrySphere, new THREE.MeshLambertMaterial({
            color: self.color(index),
            opacity: 0.5,
            transparent: true
          }));
          circle.name = content;
          circle.layers.set(index);
          circle.position.set(xscale(item.x), yscale(item.y), index * 500);
          self.scene.add(circle);
        });

        // 添加线
        data.links.forEach(item => {
          let material = new THREE.LineBasicMaterial({
            opacity: 0.5,
            transparent: true,
            vertexColors: true
          });
          let color1 = new THREE.Color(0x0000FF), color2 = new THREE.Color(0xFF0000);
          let geometry = new THREE.Geometry();
          geometry.vertices.push(new THREE.Vector3(xscale(item.x1), yscale(item.y1), index * 500));
          geometry.vertices.push(new THREE.Vector3(xscale(item.x2), yscale(item.y2), index * 500));
          geometry.colors.push(color1, color2);
          let line = new THREE.Line(geometry, material);
          line.layers.set(index);
          self.scene.add(line);
        });

        // 添加平面
        let planeGeometry = new THREE.PlaneGeometry(widthx, widthx, 10, 10);
        let plane = new THREE.Mesh(planeGeometry, new THREE.MeshLambertMaterial({
          color: 0x202020,
          opacity: 0.5,
          transparent: true,
          side: THREE.DoubleSide
        }));
        plane.position.x = 0;
        plane.position.y = 0;
        plane.position.z = index * 500;
        plane.name = 'plane';
        plane.setopacity = 0.5;
        plane.layers.set(index);
        self.scene.add(plane);
        self.plane.push(plane);

        // label
        let earthDiv = document.createElement('div');
        earthDiv.className = `label th${index}`;
        earthDiv.textContent = `${content}`;
        earthDiv.style.marginTop = '-1em';
        let earthLabel = new CSS2DObject(earthDiv);
        earthLabel.position.set(0, 0, 0);
        plane.add(earthLabel);
      },
      onWindowResize() {
        let self = this;
        self.camera.aspect = self.width / self.height;
        self.camera.updateProjectionMatrix();
        self.renderer.setSize(self.width, self.height);
      },
      onDocumentMouseMove(event) {
        let self = this;
        event.preventDefault();
        self.mouse.x = (event.offsetX / self.width) * 2 - 1;
        self.mouse.y = -(event.offsetY / self.height) * 2 + 1;
      },
      getColor() {
        return d3.scaleOrdinal(d3.schemeCategory10);
      },
      animate() {
        this.animateId = requestAnimationFrame(this.animate);
        this.controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
        this.render();
      },
      render() {
        let self = this;
        /*交互开始*/
        self.raycaster.setFromCamera(self.mouse, self.camera);
        let intersects = self.raycaster.intersectObjects(self.scene.children);
        // 有目标被选中
        if (intersects.length > 0) {
          if (self.InterSelected != intersects[0].object) {
            if (self.InterSelected)
              self.InterSelected.material.opacity = self.InterSelected.currentOpacity;

            self.InterSelected = intersects[0].object;
            if (self.InterSelected.name == 'plane') {
              self.InterSelected.currentOpacity = self.InterSelected.setopacity;
              self.InterSelected.material.opacity = self.InterSelected.setopacity;
            } else {
              self.InterSelected.currentOpacity = self.InterSelected.material.opacity;
              self.InterSelected.material.opacity = 1;
            }
          }
        } else { // 没有目标被选中
          if (self.InterSelected) // 变为原来的样式
            self.InterSelected.material.opacity = self.InterSelected.currentOpacity;
          self.InterSelected = null;
        }
        /*交互结束*/
        if (self.flag && self.state[0] && self.state[1] && self.state[2]) {
          self.flag = false;
          self.commonNode(self.level1.slice(0, 2), self.level2.slice(2, 4), 1, 2);
          self.commonNode(self.level1.slice(2, 4), self.level0.slice(0, 2), 1, 0);
          self.commonNode(self.level0.slice(2, 4), self.level2.slice(0, 2), 0, 2);
        }
        self.renderer.render(self.scene, self.camera);
        self.labelRenderer.render(self.scene, self.camera);
      },
      commonNode(data1, data2, level1, level2) {
        let self = this;
        let index = 0;
        while (index < data1.length) {
          let position1 = {}, position2 = {};
          position1 = {
            x: data1[index].x,
            y: data1[index].y,
            z: level1 * 500,
            groups: level1
          };
          position2 = {
            x: data2[index].x,
            y: data2[index].y,
            z: level2 * 500,
            groups: level2
          };
          self.drawLine(position1, position2);
          index++;
        }
      },
      drawLine(p1, p2) {
        let self = this;
        let material = new THREE.LineBasicMaterial({
          opacity: 0.5,
          transparent: true,
          vertexColors: true // 支持颜色插值
        });
        let color1 = new THREE.Color(self.color(p1.groups)), color2 = new THREE.Color(self.color(p2.groups));

        // 声明一个几何体 给几何体添加位置节点和颜色
        let geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(p1.x, p1.y, p1.z));
        geometry.vertices.push(new THREE.Vector3(p2.x, p2.y, p2.z));
        geometry.colors.push(color1, color2);
        let line = new THREE.Line(geometry, material);
        line.linename = `${p1.groups}_${p2.groups}`;
        line.layers.set(3); //  要设置为3 默认为0
        self.scene.add(line);
        self.commonNodes.push(line);
      },
      guiInit() {
        let self = this;
        self.layers = {链路: true, 网络: true, 应用: true, 透明度: 0.5};
        const gui = new dat.GUI();
        gui.add(self.layers, '链路').onChange(value => {
          self.camera.layers.toggle(0);
          self.lableToggle(0, value);
          self.lineToggle();
        });
        gui.add(self.layers, '网络').onChange(value => {
          self.camera.layers.toggle(1);
          self.lableToggle(1, value);
          self.lineToggle();
        });
        gui.add(self.layers, '应用').onChange(value => {
          self.camera.layers.toggle(2);
          self.lableToggle(2, value);
          self.lineToggle();
        });
        // 非常慢
        // gui.add(self.layers, '透明度', 0, 1).min(0).step(0.01).onChange(value => {
        //   window.event ? window.event.cancelBubble = true : e.stopPropagation();
        //   self.plane.forEach(item => {
        //     item.setopacity = value;
        //   })
        // });
        document.getElementById('Multilayer').appendChild(gui.domElement);
      },
      /*切换标签*/
      lableToggle(layer, isShow) {
        isShow === true ?
          document.getElementsByClassName(`label th${layer}`)[0].style.visibility = 'visible' :
          document.getElementsByClassName(`label th${layer}`)[0].style.visibility = 'hidden'
      },
      /*切换线条*/
      lineToggle() {
        let self = this;
        let level = [self.layers.链路, self.layers.网络, self.layers.应用];
        self.commonNodes.forEach(item => {
          let [first, second] = item.linename.split('_');
          if (level[first] && level[second]) {
            item.visible = true;
          } else {
            item.visible = false;
          }
        })
      },
    }
  };

</script>
<style scoped>
  #Multilayer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 0; /* to not conflict with dat.gui */
  }

  #Multilayer >>> .labelDiv {
    color: #FFF;
    font-family: sans-serif;
    padding: 2px;
    background: rgba(32, 32, 32, 0.4);
  }

  #Multilayer >>> .dg {
    position: absolute !important;
    right: 0 !important;
    top: 0 !important;
  }
</style>

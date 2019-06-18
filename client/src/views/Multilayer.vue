<template>
  <div id="Multilayer" ref="Multilayer">
  </div>
</template>
<script>
  import * as d3 from "d3";
  import * as dat from "dat.gui";
  import * as THREE from 'three';
  import TrackballControls from 'three-trackballcontrols';
  import {CSS2DRenderer, CSS2DObject} from 'three-css2drender';
  // import './event2.js'

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
	 let self = this;
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
        self.commonNodes = null,
        self.common = {},
        self.selectNodeLink = null,
        self.mylinks = [],
        self.lightHigh = [];
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
          self.commonNodes = [],
          self.common = {},
          self.selectNodeLink = null,
          self.mylinks = [],
          self.lightHigh = [];


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
        self.camera.position.z = 2300;
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
        // document.getElementById("Multilayer").addEventListener('mousemove', self.onDocumentMouseMove, false);
        document.getElementById("Multilayer").addEventListener('mousedown', self.onDocumentMouseDown, false);
      },
      webgl() {
        let self = this;
        self.flag = true;
        self.state[0] = false;
        self.state[1] = false;
        self.state[2] = false;
        self.scene.children = self.scene.children.slice(0, 1);
        $(".labelDiv").remove();

        let Url = "get-multi-layer-data";
        let paramsObj1 = {
          layout_type: 'rt_circular',
          network_level: 1
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
          self[`level_${index}_nodes`] = data.nodes;
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
            opacity: 0.4,
            transparent: true
          }));
          circle.name = content;
          circle.cname = item.id;
          circle.layers.set(index);
          circle.position.set(xscale(item.x), yscale(item.y), index * 500);
          self.scene.add(circle);
        });


        // 添加线
        data.links.forEach(item => {
          let material = new THREE.LineBasicMaterial({
            opacity: 0.3,
            transparent: true,
            // vertexColors: true,
            color: '#7d7d7d'
          });
          // let color1 = new THREE.Color(0x0000FF), color2 = new THREE.Color(0xFF0000);
          let geometry = new THREE.Geometry();
          geometry.vertices.push(new THREE.Vector3(xscale(item.x1), yscale(item.y1), index * 500));
          geometry.vertices.push(new THREE.Vector3(xscale(item.x2), yscale(item.y2), index * 500));
          // geometry.colors.push(color1, color2);
          // geometry.colors= color1;
          let line = new THREE.Line(geometry, material);
          line.source = item.source;
          line.target = item.target;
          line.type = 'line';
          line.level = index + 1;
          line.lname = `${index + 1}_${item.id}`;
          line.layers.set(index);
          self.scene.add(line);
          self.mylinks.push(line);
        });

        // 添加平面
        let planeGeometry = new THREE.PlaneGeometry(widthx, widthx, 10, 10);
        let plane = new THREE.Mesh(planeGeometry, new THREE.MeshLambertMaterial({
          color: 0x202020,
          opacity: 0.4,
          transparent: true,
          side: THREE.DoubleSide
        }));
        plane.position.x = 0;
        plane.position.y = 0;
        plane.position.z = index * 500;
        plane.name = 'plane';
        plane.setopacity = 0.4;
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
      onDocumentMouseDown(event) {
        let self = this;
        event.preventDefault();
        self.mouse.x = (event.offsetX / self.width) * 2 - 1;
        self.mouse.y = -(event.offsetY / self.height) * 2 + 1;

        /*交互开始*/
        self.raycaster.setFromCamera(self.mouse, self.camera);
        let intersects = self.raycaster.intersectObjects(self.scene.children);
        // 有目标被选中
        if (intersects.length > 0) {
          if (self.InterSelected != intersects[0].object) {
            if (self.InterSelected)
              self.InterSelected.material.opacity = self.InterSelected.currentOpacity;
            self.InterSelected = intersects[0].object;
            self.InterSelected.common = false;
            if (self.InterSelected.name == 'plane') {
              self.InterSelected.currentOpacity = self.InterSelected.setopacity;
              self.InterSelected.material.opacity = self.InterSelected.setopacity;
            } else if (self.InterSelected.type == 'line') {
              self.InterSelected.currentOpacity = self.InterSelected.material.opacity;
              self.InterSelected.material.opacity = 1;
              self.InterSelected.material.color.setHex(0xffffff);

              for (let item in self.common) {
                if (self.common[item].includes(self.InterSelected.source) && self.common[item].includes(self.InterSelected.target)) {
                  let sub = item.split('');
                  let findLevel = self.InterSelected.level == sub[1] ? sub[0] : sub[1];
                  let common = [self.InterSelected.source, self.InterSelected.target];
                  self.InterSelected.common = true;
                  let Url = "getLink";
                  let paramsObj1 = {
                    common: common,
                    network_level: +findLevel
                  };
                  let formData = new URLSearchParams();
                  formData.append("params", JSON.stringify(paramsObj1));

                  self.$api.get(Url, formData, data => {
                    data.link.forEach(item1 => {
                      for (let i = 0; i < self.mylinks.length; i++) {
                        if (item1 == self.mylinks[i].lname) {
                          self.lightHigh.push(self.mylinks[i]);
                          self.mylinks[i].material.opacity = 1;
                          break;
                        }
                      }
                    });
                    self.commonNodes.forEach(item => {
                      if (common.includes(item.obj)) {
                        self.lightHigh.push(item);
                        item.material.opacity = 1
                      }
                    });

                    self.lightHigh.push(self.InterSelected)

                  }, error => {
                    console.log('fail');
                  });
                }
              }

            } else {
              self.InterSelected.currentOpacity = self.InterSelected.material.opacity;
              self.InterSelected.material.opacity = 1;
            }
          }
        } else { // 没有目标被选中
          if (self.InterSelected && !self.InterSelected.common) {
            self.InterSelected.material.opacity = self.InterSelected.currentOpacity;
          }

          if (!self.layers.show && self.InterSelected) {
            self.InterSelected.material.opacity = self.InterSelected.currentOpacity;
          }
          self.InterSelected = null;
          if (!self.layers.show && self.lightHigh.length) {
            self.lightHigh.forEach(item => {
              if (item.material) {
                item.material.opacity = 0.3;
              }
            });
            self.lightHigh = [];
          }
        }
        /*交互结束*/

      }
      ,
      getColor() {
        return d3.scaleOrdinal(d3.schemeCategory10);
      }
      ,
      animate() {
        this.animateId = requestAnimationFrame(this.animate);
        this.controls.update(); // only required if controls.enableDamping = true, or if controls.autoRotate = true
        this.render();
      }
      ,
      render() {
        let self = this;
        // /*交互开始*/
        // self.raycaster.setFromCamera(self.mouse, self.camera);
        // let intersects = self.raycaster.intersectObjects(self.scene.children);
        // // 有目标被选中
        // if (intersects.length > 0) {
        //   if (self.InterSelected != intersects[0].object) {
        //     if (self.InterSelected)
        //       self.InterSelected.material.opacity = self.InterSelected.currentOpacity;
        //
        //     self.InterSelected = intersects[0].object;
        //     if (self.InterSelected.name == 'plane') {
        //       self.InterSelected.currentOpacity = self.InterSelected.setopacity;
        //       self.InterSelected.material.opacity = self.InterSelected.setopacity;
        //     } else {
        //       self.InterSelected.currentOpacity = self.InterSelected.material.opacity;
        //       self.InterSelected.material.opacity = 1;
        //       self.selectNodeLink.color.setHex(0xff0000);
        //     }
        //   }
        // } else { // 没有目标被选中
        //   if (self.InterSelected) // 变为原来的样式
        //     self.InterSelected.material.opacity = self.InterSelected.currentOpacity;
        //   self.InterSelected = null;
        // }
        // /*交互结束*/
        if (self.flag && self.state[0] && self.state[1] && self.state[2]) {
          self.flag = false;
          self.commonNode(self.level_1_nodes, self.level_2_nodes, 1, 2);
          self.commonNode(self.level_0_nodes, self.level_2_nodes, 0, 2);
          self.commonNode(self.level_0_nodes, self.level_1_nodes, 0, 1);
        }
        self.renderer.render(self.scene, self.camera);
        self.labelRenderer.render(self.scene, self.camera);

      }
      ,
      commonNode(data1, data2, level1, level2) {
        let self = this;
        let arr1 = data1.map(item => item.id);
        let arr2 = data2.map(item => item.id);
        let interaction = arr1.filter(v => arr2.includes(v));
        //console.log(interaction);
        self.common[`${level1 + 1}${level2 + 1}`] = interaction;
        let widthx = 1000;
        let xscale1 = d3.scaleLinear()
          .domain(d3.extent(data1, d => d.x))
          .range([-widthx / 2 + 30, widthx / 2 - 30]);
        let yscale1 = d3.scaleLinear()
          .domain(d3.extent(data1, d => d.y))
          .range([-widthx / 2 + 30, widthx / 2 - 30]);
        let xscale2 = d3.scaleLinear()
          .domain(d3.extent(data2, d => d.x))
          .range([-widthx / 2 + 30, widthx / 2 - 30]);
        let yscale2 = d3.scaleLinear()
          .domain(d3.extent(data2, d => d.y))
          .range([-widthx / 2 + 30, widthx / 2 - 30]);

        interaction.forEach(item => {
          let position1 = {}, position2 = {};
          for (let item1 of data1) {
            if (item1.id == item) {
              position1 = {x: xscale1(item1.x), y: yscale1(item1.y), z: level1 * 500, groups: level1, id: item};
              break;
            }
          }
          for (let item2 of data2) {
            if (item2.id == item) {
              position2 = {x: xscale2(item2.x), y: yscale2(item2.y), z: level2 * 500, groups: level2, id: item}
              break;
            }
          }
          self.drawLine(position1, position2);
        })
      }
      ,
      drawLine(p1, p2) {
        let self = this;
        let material = new THREE.LineBasicMaterial({
          opacity: 0.3,
          transparent: true,
          color: '#7d7d7d'
        });
        // let color1 = new THREE.Color(self.color(p1.groups)), color2 = new THREE.Color(self.color(p2.groups));

        // 声明一个几何体 给几何体添加位置节点和颜色
        let geometry = new THREE.Geometry();
        geometry.vertices.push(new THREE.Vector3(p1.x, p1.y, p1.z));
        geometry.vertices.push(new THREE.Vector3(p2.x, p2.y, p2.z));
        // geometry.colors.push(color1, color2);
        let line = new THREE.Line(geometry, material);
        line.obj = p1.id;
        line.linename = `${p1.groups}_${p2.groups}`;
        line.layers.set(3); //  要设置为3 默认为0
        self.scene.add(line);
        self.commonNodes.push(line); // 公共节点之间的连线
      }
      ,
      guiInit() {
        let self = this;
        self.layers = {
          链路: true, 网络: true, 应用: true, 透明度: 0.5, show: true
        };
        const gui = new dat.GUI();
        gui.add(self.layers, '应用').onChange(value => {
          self.camera.layers.toggle(2);
          self.lableToggle(2, value);
          self.lineToggle();
          window.event ? window.event.cancelBubble = true : e.stopPropagation();
        });

        gui.add(self.layers, '网络').onChange(value => {
          self.camera.layers.toggle(1);
          self.lableToggle(1, value);
          self.lineToggle();
          window.event ? window.event.cancelBubble = true : e.stopPropagation();
        });

        gui.add(self.layers, '链路').onChange(value => {
          self.camera.layers.toggle(0);
          self.lableToggle(0, value);
          self.lineToggle();
          window.event ? window.event.cancelBubble = true : e.stopPropagation();
        });

        gui.add(self.layers, 'show');

        // 非常慢
        // gui.add(self.layers, '透明度', 0, 1).min(0).step(0.01).onChange(value => {
        //   window.event ? window.event.cancelBubble = true : e.stopPropagation();
        //   self.plane.forEach(item => {
        //     item.setopacity = value;
        //   })
        // });
        document.getElementById('Multilayer').appendChild(gui.domElement);
      }
      ,
      /*切换标签*/
      lableToggle(layer, isShow) {
        isShow === true ?
          document.getElementsByClassName(`label th${layer}`)[0].style.visibility = 'visible' :
          document.getElementsByClassName(`label th${layer}`)[0].style.visibility = 'hidden'
      }
      ,
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
      }
      ,
    }
  };

</script>
<style scoped>
  #Multilayer {
    position: fixed;
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

  #Multilayer >>> .button {
    background-color: #1a1a1a;
    padding: 0;
  }

  #Multilayer >>> .close-button {
    display: none;
  }
</style>

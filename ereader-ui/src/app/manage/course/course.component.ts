import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-course',
  templateUrl: './course.component.html',
  styleUrls: ['./course.component.less']
})
export class CourseComponent implements OnInit {

  activeSectionIndex = 0;
  currentSection: any = null;

  course: any = { i: 1 };
  files: any = {}; // separate files from json (course)

  constructor() { }

  ngOnInit(): void { }

  submit(form: any) { }

  addSection() {
    if (!this.course.sections)
      this.course.sections = [];

    this.course.sections.push({ id: this.course.i++ });
  }

  removeSection(section: any) {
    this.course.sections.splice(this.course.sections.indexOf(section), 1);
  }

  addFile(section: any) {
    this.currentSection = section;
  }

  fileSelected($event: any) {
    const files = $event.target.files;

    if (files.length < 1 || !this.currentSection)
      return;

    if (!this.currentSection.files)
      this.currentSection.files = [];

    this.files[++this.course.i] = files[0];

    this.currentSection.files.push({
      id: this.course.i++,
      file_i: this.course.i,
      title: files[0].name,
    });
  }

  removeFile(section: any, file: any) {
    section.files.splice(section.files.indexOf(file), 1);
  }

  depth(file: any, inc: number) {
    file.depth = Math.max(0, Math.min(5, (file.depth || 0) + inc));
  }
}

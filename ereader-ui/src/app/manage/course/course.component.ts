import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, ActivatedRouteSnapshot, Router } from '@angular/router';
import { environment } from 'src/environments/environment';

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

  constructor(
    private http: HttpClient,
    private router: Router,
    private route: ActivatedRoute,
  ) {
    if (this.id)
      this.load();
  }

  get id() {
    return this.route.snapshot.params['id'];
  }

  ngOnInit(): void { }

  load() {
    this.http.get(`${environment.apiUrl}/courses/${this.id}`)
      .subscribe({
        next: (value) => this.course = value,
        error(err) {
          alert('oops!!! i could not load the data; my bad.');

          console.log(err);
        }
      });
  }

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
      id: this.course.i,
      title: files[0].name,
    });
  }

  removeFile(section: any, file: any) {
    section.files.splice(section.files.indexOf(file), 1);
  }

  depth(file: any, inc: number) {
    file.depth = Math.max(0, Math.min(5, (file.depth || 0) + inc));
  }

  submit(form: any) {
    const data = new FormData();

    data.append('model', JSON.stringify(this.course));

    this.course.sections?.forEach((s: any) => {
      s.files?.forEach((f: any) => {
        if (f.id in this.files)
          data.append(`file_id[${f.id}]`, this.files[f.id]);
      })
    });

    this.http.patch(`${environment.apiUrl}/courses`, data)
      .subscribe({
        next: (value) => this.router.navigate(['/manage']),
        error(err) {
          alert('oops!!! i could not save your work; my bad.');

          console.log(err);
        }
      });
  }

  removeCourse() {
    this.http.delete(`${environment.apiUrl}/courses/${this.course.id}`)
      .subscribe({
        next: (value) => this.router.navigate(['/manage']),
        error(err) {
          alert('oops!!! i could not remove this course; my bad.');

          console.log(err);
        }
      });
  }
}

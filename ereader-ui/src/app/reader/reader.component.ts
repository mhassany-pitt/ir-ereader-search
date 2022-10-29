import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from 'src/environments/environment';
import * as PDFObject from 'pdfobject';
import { v4 as uuidv4 } from 'uuid';

@Component({
  selector: 'app-reader',
  templateUrl: './reader.component.html',
  styleUrls: ['./reader.component.less']
})
export class ReaderComponent implements OnInit {

  course: any = {};
  toc = false;

  constructor(
    private http: HttpClient,
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
        next: (value: any) => {
          const course_pages: any[] = [];

          value.sections?.forEach((s: any) => {
            s.files?.forEach((f: any) => {
              f.page_elids = [];
              f.page_mediaboxes = {};

              const page_nums = []; // asc-sorted from 0
              for (var i = 0, l = f.pages || 0; i < l; i++)
                page_nums.push(i);

              let last_mediabox: any = null;
              page_nums.forEach((p: any) => {
                if (p in f.mediabox)
                  last_mediabox = f.mediabox[p];

                const page_elid = "ereader-p" + uuidv4();
                f.page_elids.push(page_elid);
                f.page_mediaboxes[page_elid] = last_mediabox.split(',');

                course_pages.push({
                  url: `${environment.apiUrl}/courses/${value.id}/${s.id}/${f.id}/${p}#toolbar=0&navpanes=0&scrollbar=0`,
                  elid: `#${page_elid}`
                });
              });
            });
          });

          this.course = value;

          setTimeout(() => course_pages.forEach((p: any) => PDFObject.embed(p.url, p.elid, {
            forcePDFJS: true
          })), 0);
        },
        error(err) {
          alert('oops!!! i could not load the data; my bad.');

          console.log(err);
        }
      });
  }

  scrollTo(elId: string) {
    document.querySelector('#' + elId)?.scrollIntoView({ behavior: 'smooth' });
  }
}

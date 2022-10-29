import { HttpClient } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { environment } from 'src/environments/environment';
import * as PDFObject from 'pdfobject';
import { v4 as uuidv4 } from 'uuid';
import { DomSanitizer } from '@angular/platform-browser';

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
    private sanitizer: DomSanitizer,
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
              if (f.type == 'img') {
                f.page_elids = ["ereader-p" + uuidv4()];
                f.src = `${environment.apiUrl}/courses/${value.id}/${s.id}/${f.id}/img`;
              } else if (f.type == 'html') {
                f.page_elids = ["ereader-p" + uuidv4()];
                f.src = this.sanitizer.bypassSecurityTrustResourceUrl(`${environment.apiUrl}/courses/${value.id}/${s.id}/${f.id}/html`);
              } else if (f.type == 'pdf') {
                f.page_elids = [];
                f.page_mediaboxes = {};

                const page_nums = []; // asc-sorted from 0
                for (let i = 0, l = f.pages || 0; i < l; i++)
                  page_nums.push(i);

                let last_mediabox: any = null;
                page_nums.forEach((p: any) => {
                  if (p in f.mediabox)
                    last_mediabox = f.mediabox[p];

                  const page_elid = "ereader-p" + uuidv4();
                  f.page_elids.push(page_elid);
                  f.page_mediaboxes[page_elid] = last_mediabox.split(',');

                  const f_src = `${environment.apiUrl}/courses/${value.id}/${s.id}/${f.id}/${p}#toolbar=0&navpanes=0&scrollbar=0`;
                  course_pages.push({ url: f_src, elid: `#${page_elid}` });
                });
              }
            });
          });

          this.course = value;

          setTimeout(() => course_pages.forEach((p: any) => PDFObject.embed(p.url, p.elid)), 0);
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

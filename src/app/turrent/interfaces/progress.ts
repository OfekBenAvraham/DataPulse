export interface Download {
  name: string;
  size: string;
  type: string;
  status: number;
}

export interface Upload {
  name: string;
  size: string;
  type: string;
  status: number;
}

export interface ProgressState {
  downloads: Download[];
  uploads: Upload[];
}

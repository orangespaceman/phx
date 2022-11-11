#!/usr/bin/env node

/**
 * Copy assets into static folder
 */

import copy from "copy";
import glob from "glob";
import clc from "cli-color";
import { deleteAsync } from "del";

const cwd = process.cwd();
const componentDir = "frontend/components";
const targetDir = "phx/templates/components";

function start() {
  deleteAsync([targetDir + "**/*"]).then((paths) => {
    paths.forEach((path) => {
      console.log(clc.green("Deleted: " + path.replace(cwd, "")));
    });
    findFiles();
  });
}

function findFiles() {
  glob(
    "**/*+(.html|.json)",
    {
      cwd: componentDir,
      nodir: true,
    },
    duplicate
  );
}

function duplicate(error, files) {
  if (!error) {
    copy(
      files,
      `../../${targetDir}`,
      {
        cwd: componentDir,
      },
      report
    );
  } else {
    throw error;
  }
}

function report(error, files) {
  if (!error) {
    files.forEach((file) => {
      console.log(clc.green(`Copied: ${file.relative}`));
    });
  } else {
    throw error;
  }
}

start();

# Data Model: GitHub-built AWS IDP Lambda Images

## Expected Image Contract

`config/idp/images.json` is the reviewed source of truth for the pinned
headless release. Its top-level fields define:

- `schemaVersion`, `upstreamVersion`, and `upstreamCommit`: contract and pinned
  AWS IDP source identity.
- `platform` and `architecture`: exactly `linux/arm64` and `arm64`.
- `context` and `dockerfile`: the repository-root build context and shared
  optimized Dockerfile.
- `baseImages`: immutable, digest-pinned build and Lambda base images.
- `images[]`: exactly 15 image definitions.

Each `images[]` entry contains:

- `logicalName`: logical image name used in the ECR tag and manifests.
- `sourcePath`: upstream Lambda source directory.
- `digestParameter`: digest parameter consumed by the template adapter.
- `lambdaLogicalId`: CloudFormation logical function name.
- `buildArgs`: fixed build arguments; only the MLflow entry has `INSTALL_GIT`.

The set is exact: bda-invoke-function, bda-completion-function,
bda-processresults-function, ocr-function, classification-function,
extraction-function, assessment-function, processresults-function,
summarization-function, evaluation-function, test-execution-aggregation-function,
rule-validation-function, rule-validation-orchestration-function,
mlflow-logger-function, and rule-validation-policy-classification-function.

## Image Release Manifest

The schema at `contracts/schemas/idp-image-release.schema.json` defines these fields:

| Field | Meaning |
| --- | --- |
| `schemaVersion` | Manifest contract version. |
| `releaseId` / `status` | Immutable workflow release identity and `COMPLETE` state. |
| `environment` | Protected GitHub/AWS deployment environment. |
| `aws.accountId` / `aws.region` / `aws.repositoryUri` | Registry and deployment context. |
| `source.upstreamRepository` / `source.upstreamVersion` / `source.upstreamCommit` | Locked AWS IDP source identity. |
| `source.lockSha256` / `source.imageContractSha256` / `source.overlaySha256` | Checksums of the reviewed build inputs. |
| `source.platformCommit` | Repository commit containing the contract and overlay. |
| `workflow.repository` / `workflow.ref` | GitHub source repository and protected branch. |
| `workflow.runId` / `workflow.runAttempt` / `workflow.runUrl` / `workflow.actor` | Reproducible GitHub execution evidence. |
| `builtAt` / `platform` | Release build time and required `linux/arm64` platform. |
| `images[]` | Exactly 15 image records. |
| `images[].logicalName` / `images[].sourcePath` / `images[].digestParameter` | Entry identity copied from the expected image contract. |
| `images[].repositoryUri` / `images[].tag` / `images[].digest` | Published ECR location, audit tag, and immutable OCI digest. |
| `images[].imageUri` | Repository URI plus `@sha256:<64 hex>`; deployment identity. |
| `images[].platform` | Must equal `linux/arm64`. |
| `images[].mediaType` | Accepted Docker or OCI image-manifest media type. |
| `images[].scan` | Scanner, completion status, severity policy, and evidence digest. |
| `images[].sbom` / `images[].provenance` | Attestation subjects and immutable evidence references. |

The validator rejects unknown/duplicate names, missing entries, tag-only URIs,
malformed digests, wrong account/region/repository, wrong source or overlay,
incomplete scans, and absent attestations.

## Deployment Selection

A deployment selection is a manifest path and SHA-256 checksum recorded by the
IDP output under `.local/idp-<environment>.json`. The output contains no
credentials and is ignored by Git. Selecting a prior manifest is the rollback
operation; no image build is part of rollback.

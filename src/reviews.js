// Preserve acknowledged editor actions when an older in-flight read arrives later.
export function mergeFlagEdits(flags, edits) {
  return flags.map(flag => {
    const edit=edits[flag.id];if(!edit)return flag;
    let patch=edit;
    const localTime=Date.parse(edit.reviewed_at)||0,serverTime=Date.parse(flag.reviewed_at)||0;
    if(localTime&&serverTime>localTime){patch={...edit};for(const key of ['dismissed','review_reason','reviewed_at'])delete patch[key];}
    const merged={...flag,...patch};
    if('copied_count' in edit)merged.copied_count=Math.max(Number(flag.copied_count)||0,Number(edit.copied_count)||0);
    return merged;
  });
}

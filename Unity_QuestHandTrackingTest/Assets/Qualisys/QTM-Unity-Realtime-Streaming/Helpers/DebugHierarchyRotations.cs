using System.Collections.Generic;
using UnityEngine;

namespace QualisysRealTime.Unity
{
    public class DebugHierarchyRotations : MonoBehaviour
    {
        public Color color = Color.red;
        private void OnDrawGizmos()
        {
            var transforms = new Stack<Transform>();
            transforms.Push(transform);
            while (transforms.Count > 0)
            {
                var x = transforms.Pop();
#if UNITY_EDITOR
                UnityEditor.Handles.color = color;
                UnityEditor.Handles.ArrowHandleCap(-1, x.transform.position, x.rotation, 0.04f, EventType.Repaint);
#endif
                foreach (Transform child in x)
                {
                    if (child.gameObject.activeInHierarchy)
                    {
#if UNITY_EDITOR
                        UnityEditor.Handles.DrawLine(x.position, child.position);
#endif
                        transforms.Push(child);
                    }
                }

            }
        }
    }
}
